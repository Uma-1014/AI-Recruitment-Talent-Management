from django.db import models

from candidates.models import Candidate
from jobs.models import Job


class Application(models.Model):

    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('AI_SCREENING', 'AI Screening'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEW', 'Interview'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
    ]

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='APPLIED'
    )

    # ---------------------------------------------------------
    # AI MATCHING SCORES
    # ---------------------------------------------------------

    match_score = models.FloatField(
        null=True,
        blank=True,
        help_text='Overall AI-generated candidate-job matching score.'
    )

    skills_score = models.FloatField(
        null=True,
        blank=True,
        help_text='AI-generated skills similarity score.'
    )

    experience_score = models.FloatField(
        null=True,
        blank=True,
        help_text='AI-generated experience matching score.'
    )

    education_score = models.FloatField(
        null=True,
        blank=True,
        help_text='AI-generated education matching score.'
    )

    recommendation = models.CharField(
        max_length=50,
        blank=True,
        help_text='AI-generated recruitment recommendation.'
    )

    # ---------------------------------------------------------
    # APPLICATION INFORMATION
    # ---------------------------------------------------------

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    notes = models.TextField(
        blank=True
    )


    class Meta:

        ordering = ['-applied_at']

        unique_together = [
            'candidate',
            'job'
        ]


    def __str__(self):

        return (
            f'{self.candidate.full_name} - '
            f'{self.job.title}'
        )
