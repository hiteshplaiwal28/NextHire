import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from jobs.models import Job
from resumes.models import Resume

from ml_engine.matching.scorer import calculate_score

job = Job.objects.latest("id")

from ml_engine.matching.ranking import rank_candidates

ranked = rank_candidates(
    job,
    Resume.objects.all()
)

print(f"\nJob: {job.title}")
print("=" * 50)

for i, item in enumerate(ranked, start=1):

    resume = item["candidate"]

    print(f"Rank #{i}")
    print(f"Candidate : {resume.candidate_name}")
    print(f"Score     : {item['score']}")
    print("-" * 50)