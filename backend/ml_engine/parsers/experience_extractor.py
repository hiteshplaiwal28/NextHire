import re


def extract_experience(text):

    text = text.lower()

    if "fresher" in text:
        return "0"

    patterns = [

        r"(\d+)\+?\s*years",

        r"(\d+)\+?\s*year",

        r"(\d+)\s*yrs",

        r"(\d+)\s*yr"

    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group(1)

    return "0"