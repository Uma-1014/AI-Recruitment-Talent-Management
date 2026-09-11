from django.contrib import admin
from .models import CandidateMatch


@admin.register(CandidateMatch)
class CandidateMatchAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'job',
        'match_score',
        'skills_score',
        'experience_score',
        'education_score',
        'recommendation',
        'created_at',
    )

    search_fields = (
        'candidate__full_name',
        'job__title',
        'recommendation',
    )

    list_filter = (
        'recommendation',
        'created_at',
    )
