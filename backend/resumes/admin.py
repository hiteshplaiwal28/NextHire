from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        "candidate_name",
        "email",
        "phone",
        "uploaded_at",
    )

    readonly_fields = (
        "candidate_name",
        "email",
        "phone",
        "skills",
        "education",
    )

    def get_fields(self, request, obj=None):
        if obj is None:
            # Add page
            return ["resume"]

        # Edit page
        return [
            "resume",
            "candidate_name",
            "email",
            "phone",
            "skills",
            "education",
        ]