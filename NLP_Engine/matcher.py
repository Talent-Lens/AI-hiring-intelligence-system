def calculate_weighted_score(resume_skills, required_skills, preferred_skills):
    resume_set = set(resume_skills)

    if not required_skills:
        return 0

    required_matches = resume_set & set(required_skills)
    preferred_matches = resume_set & set(preferred_skills)

    required_score = (len(required_matches) / len(required_skills)) * 70
    preferred_score = (len(preferred_matches) / len(preferred_skills)) * 30 if preferred_skills else 0

    total_score = required_score + preferred_score

    return round(total_score, 2)