from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):

    # Recruiter who uploaded the resume
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    candidate_name = models.CharField(
        max_length=200,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    skills = models.JSONField(
        default=list,
        blank=True
    )

    education = models.JSONField(
        default=list,
        blank=True
    )

    experience = models.CharField(
        max_length=100,
        blank=True
    )

    resume = models.FileField(
        upload_to="resumes/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.candidate_name:
            return self.candidate_name

        return "Resume"