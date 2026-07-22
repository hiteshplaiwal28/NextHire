def calculate_score(job, resume):

    # -----------------------------
    # Normalize Skills
    # -----------------------------

    job_skills = {
        s.strip().lower()
        for s in (job.required_skills or [])
        if s
    }

    resume_skills = {
        s.strip().lower()
        for s in (resume.skills or [])
        if s
    }

    matched_skills = sorted(job_skills & resume_skills)

    # -----------------------------
    # Skill Score (70)
    # -----------------------------

    if job_skills:
        skill_score = (len(matched_skills) / len(job_skills)) * 70
    else:
        skill_score = 0

    # -----------------------------
    # Education Score (20)
    # -----------------------------

    education_score = 0

    if job.education and resume.education:

        resume_edu = " ".join(resume.education).lower()

        if job.education.lower() in resume_edu:
            education_score = 20

    # -----------------------------
    # Experience Score (10)
    # -----------------------------

    experience_score = 10

    total = round(
        skill_score +
        education_score +
        experience_score,
        2
    )

    return {
        "score": total,
        "matched_skills": matched_skills,
        "skill_score": round(skill_score, 2),
        "education_score": education_score,
        "experience_score": experience_score,
        "total_required_skills": len(job_skills)
    }