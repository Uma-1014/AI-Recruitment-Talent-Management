from django.db import models
from candidates.models import Candidate
from jobs.models import Job


class CandidateMatch(models.Model):

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='ai_matches'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='ai_matches'
    )

    match_score = models.FloatField()

    skills_score = models.FloatField(default=0)

    experience_score = models.FloatField(default=0)

    education_score = models.FloatField(default=0)

    recommendation = models.CharField(
        max_length=50,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f'{self.candidate.full_name} → '
            f'{self.job.title} ({self.match_score:.1f}%)'
        )