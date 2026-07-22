import re


DEGREES = [
    "B.Tech",
    "Bachelor",
    "M.Tech",
    "Master",
    "B.E",
    "M.E",
    "BCA",
    "MCA",
    "B.Sc",
    "M.Sc",
    "PhD",
    "Intermediate",
    "Matriculation"
]


def extract_education(text):

    education = []

    for degree in DEGREES:

        if re.search(re.escape(degree), text, re.IGNORECASE):
            education.append(degree)

    return education