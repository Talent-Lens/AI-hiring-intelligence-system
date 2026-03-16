def generate_candidate_insights(match_result):

    strengths = []
    weaknesses = []
    recommendations = []

    rule_score = match_result["rule_score"]
    semantic_score = match_result["semantic_score"]
    missing_skills = match_result["missing_required"]

    # Strengths
    if rule_score > 0.7:
        strengths.append("Strong skill match with required technologies")

    if semantic_score > 0.5:
        strengths.append("High semantic similarity with job description")

    if not missing_skills:
        strengths.append("No critical skill gaps")

    # Weaknesses
    for skill in missing_skills:
        weaknesses.append(f"Missing required skill: {skill}")

    # Recommendations
    if missing_skills:
        recommendations.append(
            "Improve skills in: " + ", ".join(missing_skills)
        )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }