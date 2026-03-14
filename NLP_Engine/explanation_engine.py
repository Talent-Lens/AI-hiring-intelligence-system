def generate_candidate_insights(result, gap):

    insights = []

    matched = gap.get("matched_skills", [])
    missing = gap.get("missing_skills", [])
    experience = result.get("total_experience", 0)
    semantic_score = result.get("semantic_score", 0)

    # Skill strength
    if len(matched) >= 4:
        insights.append("Strong match on required skills")

    elif len(matched) >= 2:
        insights.append("Moderate skill match")

    else:
        insights.append("Weak skill alignment")

    # Missing skills
    if missing:
        insights.append(f"Missing skills: {', '.join(missing)}")

    # Experience insight
    if experience >= 10:
        insights.append(f"High experience ({experience} years)")

    elif experience >= 3:
        insights.append(f"Moderate experience ({experience} years)")

    else:
        insights.append(f"Low experience ({experience} years)")

    # Semantic similarity insight
    if semantic_score > 0.6:
        insights.append("Strong semantic alignment with job description")

    elif semantic_score > 0.4:
        insights.append("Moderate semantic similarity with job description")

    else:
        insights.append("Low semantic similarity with job description")

    return insights