import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from jobs.models import Job
from ml_engine.jd_parser.pdf_parser import extract_text_from_pdf
from ml_engine.jd_parser.skill_extractor import extract_skills
from ml_engine.jd_parser.education_extractor import extract_education
from ml_engine.jd_parser.experience_extractor import extract_experience
job = Job.objects.latest("id")

if job and job.jd_file:
    pdf_path = job.jd_file.path

    print("Reading:", pdf_path)

    text = extract_text_from_pdf(pdf_path)

    print("\n===== Job Description =====\n")
    print(text)

    print("\nSkills:")
    print(extract_skills(text))

    print("\nEducation:")
    print(extract_education(text))

    print("\nExperience:")
    print(extract_experience(text))
else:
    print("No Job Description found.")