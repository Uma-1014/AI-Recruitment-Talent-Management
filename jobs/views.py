from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import JobForm
from .models import Job


@login_required
def job_list(request):
    jobs = Job.objects.filter(
        recruiter=request.user
    ).order_by('-created_at')

    return render(
        request,
        'jobs/job_list.html',
        {
            'jobs': jobs,
        }
    )


@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()

            return redirect('job_list')

    else:
        form = JobForm()

    return render(
        request,
        'jobs/job_form.html',
        {
            'form': form,
        }
    )