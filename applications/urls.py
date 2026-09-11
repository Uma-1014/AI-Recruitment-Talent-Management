from django.urls import path

from . import views


urlpatterns = [
    # Candidate job browsing
    path(
        'jobs/',
        views.job_list,
        name='application_job_list'
    ),

    # Candidate applies for a specific job
    path(
        'apply/<int:job_id>/',
        views.apply_job,
        name='apply_job'
    ),

    # Application submission success
    path(
        'success/',
        views.application_success,
        name='application_success'
    ),

    # Candidate's submitted applications
    path(
        'my/',
        views.my_applications,
        name='my_applications'
    ),

    # Recruiter application management
    path(
        'manage/',
        views.manage_applications,
        name='manage_applications'
    ),
]