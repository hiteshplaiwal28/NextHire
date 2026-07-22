from ml_engine.parsers.name_extractor import extract_name
from ml_engine.parsers.information_extractor import (
    extract_email,
    extract_phone,
)
from ml_engine.parsers.skill_extractor import extract_skills
from ml_engine.parsers.education_extractor import extract_education
from ml_engine.parsers.experience_extractor import extract_experience


def parse_resume(text):

    data = {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "skills": extract_skills(text),

        "education": extract_education(text),

        "experience": extract_experience(text),

    }

    return data