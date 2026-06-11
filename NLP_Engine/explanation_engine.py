def generate_candidate_insights(result, gap):
    # DEBUG: VERSION 1.0.8
    strengths = []
    weaknesses = []
    recommendations = []

    matched = gap.get("matched_skills", [])
    missing = gap.get("missing_skills", [])
    experience = result.get("total_experience", 0)
    semantic_score = result.get("semantic_score", 0)
    rule_score = result.get("rule_score", 0)

    # 1. Strengths
    if matched:
        strengths.append(f"Strong match for tech: {', '.join(matched[:4])}")
        if len(matched) >= 3:
            strengths.append("Verified technical depth in core requirements")

    if experience >= 3:
        strengths.append(f"Solid tenure of {experience} years detected")
    
    if semantic_score > 0.5:
        strengths.append("High context alignment with job description")

    # 2. Weaknesses
    if missing:
        weaknesses.append(f"Skill gaps identified: {', '.join(missing[:3])}")
        recommendations.append(f"Recommended Upskill: {', '.join(missing)}")
    
    if experience < 2:
        weaknesses.append(f"Candidate has lower experience than typical ({experience} years)")

    if semantic_score < 0.4:
        weaknesses.append("Contextual alignment could be improved")

    # Final logic to ensure NOT EMPTY
    if not strengths: strengths.append("Candidate demonstrates basic technical eligibility")
    if not weaknesses and missing: weaknesses.append("Technical assessment recommended for gaps")
    if not recommendations: recommendations.append("Proceed to next stage for further verification")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }