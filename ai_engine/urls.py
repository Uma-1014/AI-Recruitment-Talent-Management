from django.urls import path

from . import views


urlpatterns = [

    path(
        'dashboard/',
        views.ai_dashboard,
        name='ai_dashboard'
    ),

    path(
        'match/<int:job_id>/',
        views.match_candidates,
        name='match_candidates'
    ),

]