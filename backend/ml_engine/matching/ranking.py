from ml_engine.matching.scorer import calculate_score


def rank_candidates(job, resumes):

    rankings = []

    for resume in resumes:

        result = calculate_score(job, resume)

        rankings.append({

            # Store the Resume object
            "candidate": resume,

            "score": result["score"],

            "matched_skills": result.get("matched_skills", []),
            "missing_skills": result.get("missing_skills", []),
            "skill_score": result.get("skill_score", 0),
            "education_score": result.get("education_score", 0),
            "experience_score": result.get("experience_score", 0),

            "skills": ", ".join(resume.skills or []),

            "education": ", ".join(resume.education or []),

            "email": resume.email,

            "phone": resume.phone,

        })

    rankings.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return rankings