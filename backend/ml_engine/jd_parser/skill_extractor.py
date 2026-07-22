import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

SKILL_FILE = os.path.join(
    BASE_DIR,
    "ml_engine",
    "datasets",
    "skills.csv"
)


def extract_skills(text):

    skills_df = pd.read_csv(SKILL_FILE)

    skills = skills_df["skill"].dropna().tolist()

    found_skills = []

    text = text.lower()

    for skill in skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(set(found_skills))