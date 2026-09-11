from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'job_type',
        'location',
        'experience_required',
        'is_active',
        'created_at',
    )

    search_fields = (
        'title',
        'description',
        'required_skills',
        'location',
    )

    list_filter = (
        'job_type',
        'is_active',
        'location',
        'created_at',
    )