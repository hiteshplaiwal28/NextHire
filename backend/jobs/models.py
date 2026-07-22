from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):

    # Recruiter who created the job
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)

    department = models.CharField(max_length=100)

    location = models.CharField(max_length=100)

    education = models.CharField(max_length=200, blank=True)

    experience = models.CharField(max_length=100, blank=True)

    salary = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    jd_file = models.FileField(
        upload_to="job_descriptions/",
        blank=True,
        null=True
    )

    # -------- AI Extracted Fields --------

    required_skills = models.JSONField(
        default=list,
        blank=True
    )

    required_education = models.JSONField(
        default=list,
        blank=True
    )

    required_experience = models.CharField(
        max_length=100,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="Open"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title