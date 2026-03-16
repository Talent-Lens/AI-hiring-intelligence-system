from NLP_Engine.skill_synonyms import normalize_skills

def analyze_skill_gap(job_data, resume_data):

    skill_weights = job_data["skill_weights"]

    resume_skills = set(normalize_skills(resume_data["skills"]))

    matched = []
    missing = []

    critical_gaps = []
    moderate_gaps = []
    minor_gaps = []

    for skill, weight in skill_weights.items():

        if skill in resume_skills:
            matched.append(skill)

        else:
            missing.append(skill)

            if weight >= 3:
                critical_gaps.append(skill)

            elif weight >= 2:
                moderate_gaps.append(skill)

            else:
                minor_gaps.append(skill)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "critical_skill_gaps": critical_gaps,
        "moderate_skill_gaps": moderate_gaps,
        "minor_skill_gaps": minor_gaps
    }