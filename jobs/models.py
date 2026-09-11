from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    JOB_TYPES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
    ]

    title = models.CharField(max_length=200)

    description = models.TextField()

    required_skills = models.TextField(
        help_text='Enter required skills separated by commas.'
    )

    education_required = models.CharField(
        max_length=200,
        blank=True
    )

    experience_required = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0
    )

    location = models.CharField(
        max_length=150,
        blank=True
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES,
        default='FULL_TIME'
    )

    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_jobs'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
