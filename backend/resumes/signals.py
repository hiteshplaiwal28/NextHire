from django.db.models.signals import post_save
from django.dispatch import receiver

from resumes.models import Resume

from ml_engine.parsers.pdf_parser import extract_text_from_pdf
from ml_engine.parsers.resume_parser import parse_resume

@receiver(post_save, sender=Resume)
def parse_uploaded_resume(sender, instance, created, **kwargs):

    # Only parse when a new resume is uploaded
    if not created:
        return

    # Resume file must exist
    if not instance.resume:
        return

    try:

        print("=" * 60)
        print("Resume Parsing Started...")
        print("File:", instance.resume.path)

        # Extract text from PDF
        text = extract_text_from_pdf(instance.resume.path)

        if not text.strip():
            print("No text found inside resume.")
            return

        # Parse Resume
        data = parse_resume(text)

        print("Parsed Data:")
        print(data)

        # Save parsed information
        instance.candidate_name = data.get("name", "")
        instance.email = data.get("email", "") or ""
        instance.phone = data.get("phone", "") or ""
        instance.skills = data.get("skills", [])
        instance.education = data.get("education", [])
        instance.experience = data.get("experience", "")

        instance.save(
            update_fields=[
                "candidate_name",
                "email",
                "phone",
                "skills",
                "education",
                "experience",
            ]
        )

        print("Resume parsed successfully.")
        print("=" * 60)

    except Exception as e:

        print("=" * 60)
        print("Resume Parsing Error")
        print(e)
        print("=" * 60)