import re
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_name(text):

    # ---------- Method 1 ----------
    # Check first 5 non-empty lines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:5]:

        # Ignore lines containing these words
        if any(word in line.lower() for word in [
            "email",
            "mobile",
            "phone",
            "github",
            "linkedin",
            "engineering",
            "computer",
            "college",
            "university",
            "institute"
        ]):
            continue

        # Accept short lines with 1-4 words
        words = line.split()

        if 1 <= len(words) <= 4:
            return line

    # ---------- Method 2 ----------
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Name Not Found"