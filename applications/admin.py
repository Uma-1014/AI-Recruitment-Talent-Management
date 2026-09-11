from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'candidate',
        'job',
        'status',
        'match_score',
        'applied_at',
    )

    search_fields = (
        'candidate__full_name',
        'candidate__email',
        'job__title',
    )

    list_filter = (
        'status',
        'applied_at',
    )
