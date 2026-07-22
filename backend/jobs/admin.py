from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "department",
        "location",
        "experience",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "department",
        "location",
    )

    search_fields = (
        "title",
        "department",
        "location",
    )

    ordering = ("-created_at",)