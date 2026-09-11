from django.contrib import admin
from .models import Candidate


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'experience_years',
        'location',
        'created_at',
    )

    search_fields = (
        'full_name',
        'email',
        'skills',
        'location',
    )

    list_filter = (
        'location',
        'created_at',
    )
