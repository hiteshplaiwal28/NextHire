import re

DEGREES = {
    "B.Tech": [
        "B.Tech",
        "BTech",
        "Bachelor of Technology"
    ],
    "B.E": [
        "B.E",
        "BE",
        "Bachelor of Engineering"
    ],
    "M.Tech": [
        "M.Tech",
        "MTech",
        "Master of Technology"
    ],
    "BCA": [
        "BCA",
        "Bachelor of Computer Applications"
    ],
    "MCA": [
        "MCA",
        "Master of Computer Applications"
    ],
    "B.Sc": [
        "B.Sc",
        "BSc",
        "Bachelor of Science"
    ],
    "M.Sc": [
        "M.Sc",
        "MSc",
        "Master of Science"
    ],
    "MBA": [
        "MBA",
        "Master of Business Administration"
    ],
    "PhD": [
        "PhD",
        "Doctor of Philosophy"
    ],
    "Intermediate": [
        "Intermediate",
        "Senior Secondary",
        "12th"
    ],
    "Matriculation": [
        "Matriculation",
        "Secondary",
        "10th"
    ]
}


def extract_education(text):

    education = []

    text = text.lower()

    for degree, keywords in DEGREES.items():
        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"

            if re.search(pattern, text):
                education.append(degree)
                break

    return education