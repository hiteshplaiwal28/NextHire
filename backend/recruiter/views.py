from django.shortcuts import render
from jobs.models import Job
from resumes.models import Resume


def dashboard(request):
    context = {
        "total_jobs": Job.objects.count(),
        "total_resumes": Resume.objects.count(),
        "jobs": Job.objects.all().order_by("-created_at"),
    }

    return render(request, "recruiter/dashboard.html", context)