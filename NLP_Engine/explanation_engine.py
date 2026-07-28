def detect_domain(matched_skills):
    domain_signals = {
        "HR": {"talent acquisition","hris","shrm-scp","sphr","onboarding","hr strategy"},
        "Finance": {"financial modeling","fp&a","gaap","ifrs","valuation","budgeting"},
        "Marketing": {"seo","sem","google analytics","content marketing","hubspot"},
        "Sales": {"b2b sales","salesforce","pipeline management","account management"},
        "Engineering": {"python","java","react","node.js","docker","kubernetes"},
        "Data": {"machine learning","sql","tableau","power bi","data analysis"},
        "Design": {"figma","ux design","ui design","prototyping","user research"},
    }
    scores = {domain: len(set(matched_skills) & signals)
              for domain, signals in domain_signals.items()}
    return max(scores, key=scores.get) if any(scores.values()) else "Professional"

def generate_candidate_insights(result, gap):
    matched = gap.get("matched_skills", [])
    missing = gap.get("missing_skills", [])
    demonstrated = result.get("demonstrated_skills", {})
    mentioned_only = result.get("mentioned_only_skills", {})
    experience = result.get("total_experience", 0)
    semantic_score = result.get("semantic_score", 0)
    rule_score = result.get("rule_score", 0)
    domain = detect_domain(matched)

    strengths = []
    weaknesses = []
    recommendations = []

    # 1. STRENGTHS
    proven_skill_names = list(demonstrated.keys()) if isinstance(demonstrated, dict) else []
    mentioned_skill_names = list(mentioned_only.keys()) if isinstance(mentioned_only, dict) else []

    if proven_skill_names:
        top_proven = ", ".join(proven_skill_names[:4])
        strengths.append(f"🏆 Proven hands-on competency in {top_proven} backed by project evidence")

    if domain and domain != "Professional":
        strengths.append(f"🎯 Strong {domain} domain alignment")

    if experience > 0:
        strengths.append(f"💼 {experience:.1f} years of relevant experience detected")

    if semantic_score >= 0.6:
        pct = int(semantic_score * 100)
        strengths.append(f"🧠 High semantic alignment ({pct}%) with job description responsibilities")

    if rule_score >= 0.7:
        strengths.append(f"⚡ Comprehensive coverage of required technical qualifications ({int(rule_score*100)}%)")

    if not strengths:
        strengths.append("Candidate demonstrates foundational eligibility for the position")

    # 2. WEAKNESSES / RISK AREAS
    if missing:
        top_missing = ", ".join(missing[:4])
        weaknesses.append(f"⚠️ Missing key job requirements: {top_missing}")

    if mentioned_skill_names:
        top_mentioned = ", ".join(mentioned_skill_names[:3])
        weaknesses.append(f"📜 Listed without project execution proof: {top_mentioned}")

    if experience < 2 and rule_score < 0.5:
        weaknesses.append("📉 Limited experience and low keyword coverage for senior-level expectations")

    if not weaknesses:
        weaknesses.append("No critical skill gaps or major risk factors identified")

    # 3. ACTIONABLE RECOMMENDATIONS
    if proven_skill_names:
        recommendations.append(f"Ask candidate to elaborate on project architecture using {proven_skill_names[0]}")

    if mentioned_skill_names:
        top_m = ", ".join(mentioned_skill_names[:3])
        recommendations.append(f"Verify practical hands-on proficiency for mentioned-only skills: {top_m}")

    if missing:
        top_miss = ", ".join(missing[:3])
        recommendations.append(f"Probe willingness and capability to quickly learn missing areas: {top_miss}")

    if not recommendations:
        recommendations.append("Proceed to technical interview / screening call to validate competency depth")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }