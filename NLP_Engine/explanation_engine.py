def generate_candidate_insights(result, gap):

    strengths = []
    weaknesses = []
    recommendations = []

    matched = gap.get("matched_skills", [])
    missing = gap.get("missing_skills", [])
    experience = result.get("total_experience", 0)
    semantic_score = result.get("semantic_score", 0)
    if matched:
        strengths.append(f"Matched skills: {', '.join(matched)}")
    # Skill match insight
    if len(matched) >= 4:
        strengths.append("Strong match on required skills")

    elif len(matched) >= 2:
        strengths.append("Moderate skill match")

    else:
        weaknesses.append("Weak skill alignment")

    # Missing skills
    if missing:
        weaknesses.append(f"Missing skills: {', '.join(missing)}")
        recommendations.append(f"Improve skills in: {', '.join(missing)}")

    # Experience insight
    if experience >= 10:
        strengths.append(f"High experience ({experience} years)")

    elif experience >= 3:
        strengths.append(f"Moderate experience ({experience} years)")

    else:
        weaknesses.append(f"Low experience ({experience} years)")

    # Semantic similarity insight
    if semantic_score > 0.6:
        strengths.append("Strong semantic alignment with job description")

    elif semantic_score > 0.4:
        strengths.append("Moderate semantic similarity with job description")

    else:
        weaknesses.append("Low semantic similarity with job description")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }