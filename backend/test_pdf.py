import os
import django
from pprint import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from resumes.models import Resume
from ml_engine.parsers.pdf_parser import extract_text_from_pdf
from ml_engine.parsers.resume_parser import parse_resume

resume = Resume.objects.latest("id")

if resume:

    pdf_path = resume.resume.path

    print("Reading:", pdf_path)

    text = extract_text_from_pdf(pdf_path)

    print("\n===== Resume Text =====\n")
    print(text)

    print("\n==============================")
    print("PARSED RESUME")
    print("==============================")

    result = parse_resume(text)

    pprint(result)

else:
    print("No resume found in database.")