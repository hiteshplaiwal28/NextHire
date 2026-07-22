import re


def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


def extract_phone(text):
    pattern = r"(\+?\d{1,3}[- ]?)?\d{10}"

    match = re.search(pattern, text)

    if match:
        return match.group().strip()

    return None