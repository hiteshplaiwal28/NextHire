import re

def extract_experience(text):
    patterns = [
        r'(\d+\+?\s*(?:-|to)?\s*\d*\+?\s*years?)',
        r'(\d+\+?\s*(?:-|to)?\s*\d*\+?\s*year)',
        r'freshers?',
        r'no experience',
    ]

    text = text.lower()

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()

    return "Not Mentioned"