from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from candidates.models import Candidate
from jobs.models import Job
from applications.models import Application

from .models import CandidateMatch
from .matching import calculate_match_score


@login_required
def ai_dashboard(request):
    """
    Main AI Recruitment Analytics Dashboard.
    """

    jobs = Job.objects.filter(
        recruiter=request.user
    ).order_by('-created_at')

    candidates = Candidate.objects.all()

    applications = Application.objects.filter(
        job__recruiter=request.user
    )

    ai_screened_applications = applications.filter(
        match_score__isnull=False
    )

    # ---------------------------------------------------------
    # BASIC STATISTICS
    # ---------------------------------------------------------

    job_count = jobs.count()
    candidate_count = candidates.count()
    application_count = applications.count()
    ai_screened_count = ai_screened_applications.count()

    # ---------------------------------------------------------
    # AVERAGE AI SCORE
    # ---------------------------------------------------------

    average_score = 0

    if ai_screened_count > 0:
        scores = [
            application.match_score
            for application in ai_screened_applications
            if application.match_score is not None
        ]

        if scores:
            average_score = round(
                sum(scores) / len(scores),
                2
            )

    # ---------------------------------------------------------
    # MATCH CATEGORY COUNTS
    # ---------------------------------------------------------

    strong_matches = ai_screened_applications.filter(
        match_score__gte=80
    ).count()

    good_matches = ai_screened_applications.filter(
        match_score__gte=60,
        match_score__lt=80
    ).count()

    potential_matches = ai_screened_applications.filter(
        match_score__gte=40,
        match_score__lt=60
    ).count()

    low_matches = ai_screened_applications.filter(
        match_score__lt=40
    ).count()

    # ---------------------------------------------------------
    # TOP CANDIDATES
    # ---------------------------------------------------------

    top_candidates = ai_screened_applications.order_by(
        '-match_score'
    )[:5]

    # ---------------------------------------------------------
    # JOB-WISE AI INSIGHTS
    # ---------------------------------------------------------

    job_insights = []

    for job in jobs:
        job_applications = applications.filter(
            job=job,
            match_score__isnull=False
        )

        job_scores = [
            application.match_score
            for application in job_applications
            if application.match_score is not None
        ]

        if job_scores:
            job_average = round(
                sum(job_scores) / len(job_scores),
                2
            )

            job_top_score = round(
                max(job_scores),
                2
            )
        else:
            job_average = 0
            job_top_score = 0

        job_insights.append({
            'job': job,
            'application_count': job_applications.count(),
            'average_score': job_average,
            'top_score': job_top_score,
        })

    # ---------------------------------------------------------
    # CONTEXT
    # ---------------------------------------------------------

    context = {
        'jobs': jobs,
        'job_count': job_count,
        'candidate_count': candidate_count,
        'application_count': application_count,
        'ai_screened_count': ai_screened_count,
        'average_score': average_score,

        'strong_matches': strong_matches,
        'good_matches': good_matches,
        'potential_matches': potential_matches,
        'low_matches': low_matches,

        'top_candidates': top_candidates,
        'job_insights': job_insights,
    }

    return render(
        request,
        'ai_engine/dashboard.html',
        context
    )


@login_required
def match_candidates(request, job_id):
    """
    Run AI candidate-job matching for a specific job.
    """

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    candidates = Candidate.objects.all()

    matches = []

    for candidate in candidates:

        result = calculate_match_score(
            candidate,
            job
        )

        match, created = CandidateMatch.objects.update_or_create(
            candidate=candidate,
            job=job,
            defaults={
                'match_score': result['match_score'],
                'skills_score': result['skills_score'],
                'experience_score': result['experience_score'],
                'education_score': result['education_score'],
                'recommendation': result['recommendation'],
            }
        )

        matches.append(match)

    # Highest AI score first
    matches.sort(
        key=lambda item: item.match_score,
        reverse=True
    )

    return render(
        request,
        'ai_engine/matches.html',
        {
            'job': job,
            'matches': matches,
        }
    )