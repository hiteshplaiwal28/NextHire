import re
import pandas as pd
from pathlib import Path

# backend directory
BASE_DIR = Path(__file__).resolve().parents[2]

SKILL_FILE = BASE_DIR / "ml_engine" / "datasets" / "skills.csv"


def extract_skills(text):

    if not SKILL_FILE.is_file():
        print(f"skills.csv not found: {SKILL_FILE}")
        return []

    skills_df = pd.read_csv(SKILL_FILE)

    skills = skills_df["skill"].dropna().tolist()

    found_skills = []

    text = text.lower()

    for skill in skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))