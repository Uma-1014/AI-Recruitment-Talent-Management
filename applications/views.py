from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from candidates.models import Candidate
from jobs.models import Job

from .models import Application
from ai_engine.matching import calculate_match_score


@login_required
def job_list(request):
    """
    Display all active jobs available for candidates.
    """

    jobs = Job.objects.filter(
        is_active=True
    ).order_by('-created_at')

    return render(
        request,
        'applications/job_list.html',
        {
            'jobs': jobs,
        }
    )


@login_required
def apply_job(request, job_id):
    """
    Allow a candidate to apply for a job.

    AI calculates the candidate-job match score
    when the application is submitted.
    """

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    candidate = Candidate.objects.filter(
        user=request.user
    ).first()

    if candidate is None:
        messages.error(
            request,
            'Please complete your candidate profile before applying.'
        )
        return redirect('candidate_profile')

    existing_application = Application.objects.filter(
        candidate=candidate,
        job=job
    ).first()

    if existing_application:
        messages.warning(
            request,
            'You have already applied for this job.'
        )
        return redirect('my_applications')

    if request.method == 'POST':

        # Run AI candidate-job matching
        result = calculate_match_score(
            candidate,
            job
        )

        Application.objects.create(
            candidate=candidate,
            job=job,
            status='APPLIED',
            match_score=result['match_score'],
            skills_score=result['skills_score'],
            experience_score=result['experience_score'],
            education_score=result['education_score'],
        )

        messages.success(
            request,
            'Application submitted successfully. AI has analyzed your profile.'
        )

        return redirect('application_success')

    return render(
        request,
        'applications/apply.html',
        {
            'job': job,
            'candidate': candidate,
        }
    )


@login_required
def application_success(request):
    """
    Application submission success page.
    """

    return render(
        request,
        'applications/application_success.html'
    )


@login_required
def my_applications(request):
    """
    Display applications submitted by the current candidate.
    """

    candidate = Candidate.objects.filter(
        user=request.user
    ).first()

    if candidate is None:
        applications = []
    else:
        applications = Application.objects.filter(
            candidate=candidate
        ).select_related(
            'job'
        ).order_by('-applied_at')

    return render(
        request,
        'applications/my_applications.html',
        {
            'applications': applications,
        }
    )


@login_required
def manage_applications(request):
    """
    Recruiter application management page.

    Recruiters can:
    - View applications for their jobs
    - View AI match scores
    - View AI recommendations
    - Change application status
    - Select candidates
    - Reject candidates
    """

    applications = Application.objects.filter(
        job__recruiter=request.user
    ).select_related(
        'candidate',
        'job'
    ).order_by(
        '-match_score',
        '-applied_at'
    )

    if request.method == 'POST':

        application_id = request.POST.get(
            'application_id'
        )

        new_status = request.POST.get(
            'status'
        )

        valid_statuses = dict(
            Application.STATUS_CHOICES
        )

        if new_status not in valid_statuses:

            messages.error(
                request,
                'Invalid application status.'
            )

            return redirect(
                'manage_applications'
            )

        application = get_object_or_404(
            Application,
            id=application_id,
            job__recruiter=request.user
        )

        application.status = new_status
        application.save()

        messages.success(
            request,
            f'Application status updated to '
            f'{valid_statuses[new_status]}.'
        )

        return redirect(
            'manage_applications'
        )

    return render(
        request,
        'applications/manage_applications.html',
        {
            'applications': applications,
        }
    )