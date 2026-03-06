from NLP_Engine.skill_synonym import normalize_skills

def analyze_skill_gap(job_data, resume_data):
    required_skills = set(normalize_skills(job_data["required_skills"]))
    skill_weights = job_data["skill_weights"]

    resume_skills = resume_data["skills"]

    matched = required_skills.intersection(resume_skills)
    missing = required_skills.difference(resume_skills)

    critical_gaps = []
    moderate_gaps = []
    minor_gaps = []

    for skill in missing:
        weight = skill_weights.get(skill, 1)

        if weight == 3:
            critical_gaps.append(skill)
        elif weight == 2:
            moderate_gaps.append(skill)
        else:
            minor_gaps.append(skill)

    return {
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "critical_skill_gaps": critical_gaps,
        "moderate_skill_gaps": moderate_gaps,
        "minor_skill_gaps": minor_gaps
    }