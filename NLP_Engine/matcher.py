import re
from sklearn.metrics.pairwise import cosine_similarity
from NLP_Engine.skill_gap_analyzer import analyze_skill_gap
from NLP_Engine.skill_synonyms import normalize_skills
from NLP_Engine.skill_similarity import find_semantic_skill_matches
from NLP_Engine.explanation_engine import generate_candidate_insights
from NLP_Engine.skill_extractor import classify_skills_by_section
from NLP_Engine.evidence_mapper import extract_semantic_evidence
from NLP_Engine.skill_db import MASTER_SKILLS
from NLP_Engine.experience_extractor import extract_required_experience
SOFT_SKILLS = MASTER_SKILLS["soft_skills"]
# ----------------------------
# LOAD MODEL (Singleton)
# ----------------------------
from NLP_Engine.model_singleton import get_model
model = get_model()

# ----------------------------
# SEMANTIC SCORE
# ----------------------------
_job_embedding_cache = {}
_resume_embedding_cache = {}

def compute_semantic_score(job_text, resume_text):
    if job_text not in _job_embedding_cache:
        _job_embedding_cache[job_text] = model.encode(job_text, convert_to_tensor=False, show_progress_bar=False)

    if resume_text not in _resume_embedding_cache:
        _resume_embedding_cache[resume_text] = model.encode(resume_text, convert_to_tensor=False, show_progress_bar=False)

    job_embedding = _job_embedding_cache[job_text]
    resume_embedding = _resume_embedding_cache[resume_text]

    similarity = cosine_similarity(
        [job_embedding],
        [resume_embedding]
    )[0][0]

    return float(similarity)


# ----------------------------
# RULE-BASED SCORE
# ----------------------------
def compute_rule_score(required_skills, resume_skills, skill_weights):

    if not required_skills:
        return 0.0, [], [], {}, 0

    matched_required = required_skills.intersection(resume_skills)
    missing_required = required_skills.difference(resume_skills)

    # ---------------- SEMANTIC SKILL MATCH ----------------
    semantic_skill_matches = find_semantic_skill_matches(
        missing_required,
        resume_skills
    )

    for req_skill, res_skill in semantic_skill_matches.items():
        matched_required.add(req_skill)
        if req_skill in missing_required:
            missing_required.discard(req_skill)

    total_required = len(required_skills)
    if total_required > 0:
        skill_coverage = len(matched_required) / total_required
    else:
        skill_coverage = 0

    matched_required = list(matched_required)
    missing_required = list(missing_required)

    total_weight = sum(skill_weights.get(skill, 1) for skill in required_skills)

    if total_weight == 0:
        return 0.0, list(matched_required), list(missing_required), semantic_skill_matches, skill_coverage

    matched_weight = sum(skill_weights.get(skill, 1) for skill in matched_required)

    rule_score = matched_weight / total_weight

    return rule_score, list(matched_required), list(missing_required), semantic_skill_matches, skill_coverage



# ----------------------------
# MATCH FUNCTION
# ----------------------------
def match_resume_to_job(
    job_data,
    resume_data,
    semantic_weight=0.4,
    rule_weight=0.6
):

    # Dynamic weight adjustment based on JD complexity
    skill_count = len(job_data["skill_weights"])

    if skill_count >= 15:
        semantic_weight, rule_weight = 0.25, 0.75
    elif skill_count >= 8:
        semantic_weight, rule_weight = 0.35, 0.65
    else:
        semantic_weight, rule_weight = 0.50, 0.50

    # Safety check
    if round(semantic_weight + rule_weight, 2) != 1.0:
        raise ValueError("semantic_weight + rule_weight must equal 1.0")

    job_text = job_data["text"]
    required_skills = set(normalize_skills(job_data["skill_weights"]))

    resume_text = resume_data["text"]
    resume_skills = set(normalize_skills(resume_data["skills"]))

    # 1️⃣ Rule Score
    rule_score, matched_required, missing_required, semantic_skill_matches, skill_coverage = compute_rule_score(
        required_skills,
        resume_skills,
        job_data["skill_weights"],
    )

    # Classified Skills & Evidence Mapping
    categorized_skills = classify_skills_by_section(resume_text, required_skills, semantic_skill_matches)
    semantic_evidence = extract_semantic_evidence(job_text, resume_text)
    skill_gap = {
    "matched_skills": matched_required,
    "missing_skills": missing_required,
    "critical_skill_gaps": [s for s in missing_required if job_data["skill_weights"].get(s, 0) >= 3],
    "moderate_skill_gaps": [s for s in missing_required if 2 <= job_data["skill_weights"].get(s, 0) < 3],
    "minor_skill_gaps": [s for s in missing_required if job_data["skill_weights"].get(s, 0) < 2],
}

    # 2️⃣ Semantic Score
    semantic_score = compute_semantic_score(job_text, resume_text)

    # 3️⃣ Hybrid Base Score
    base_score = (semantic_weight * semantic_score) + \
                 (rule_weight * rule_score)

    # ---------------- EXPERIENCE BONUS ----------------
    experience = resume_data.get("total_experience", 0)
    experience_source = resume_data.get("experience_source", "calculated")
    required_experience = extract_required_experience(job_data["text"])["years"]

    # exp_ratio = 1.0 → candidate meets bar exactly
    # exp_ratio > 1.0 → overqualified (capped at 1.5x)
    # exp_ratio < 1.0 → under the bar → no bonus
    exp_ratio = min(experience / max(required_experience, 1), 1.5)

    if exp_ratio >= 1.0:
        full_bonus = min((exp_ratio - 1.0) * 0.08, 0.08)
    # "unknown" source means no real signal was found at all — don't reward it.
    # "claimed" (a stated "X years experience" with no date ranges) gets a
    # reduced bonus since it's unverified. "calculated" (real date ranges
    # found in the resume) gets the full bonus.
        if experience_source == "unknown":
            experience_bonus = 0.0
        elif experience_source == "claimed":
            experience_bonus = full_bonus * 0.5
        else:
            experience_bonus = full_bonus
    else:
        experience_bonus = 0.0

    pre_penalty_score = base_score + experience_bonus

    # ---------------- MANDATORY SKILL LOGIC ----------------
    mandatory_skills = [
        skill for skill, weight in job_data["skill_weights"].items()
        if weight == 3
    ]

    mandatory_missing = [
        skill for skill in missing_required
        if skill in mandatory_skills
    ]

    # Mandatory Match Bonus
    if mandatory_skills and len(mandatory_missing) == 0:
        pre_penalty_score += 0.05

    # ---------------- TIERED PENALTY SYSTEM ----------------
    penalty_multiplier = 1.0

    if mandatory_skills:
        penalty_ratio = len(mandatory_missing) / len(mandatory_skills)

        if penalty_ratio >= 0.75:
            penalty_multiplier = 0.4
        elif penalty_ratio >= 0.5:
            penalty_multiplier = 0.6
        elif penalty_ratio > 0:
            penalty_multiplier = 0.8

    if rule_score < 0.20 and semantic_score > 0.30:
        penalty_multiplier = max(penalty_multiplier, 0.75)

    final_score = (pre_penalty_score * penalty_multiplier)

    # ---------------- MATCH CATEGORY ----------------
    if final_score >= 0.75:
        category = "Strong Match"
    elif final_score >= 0.50:
        category = "Moderate Match"
    elif final_score >= 0.30:
        category = "Weak Match"
    else:
        category = "Very Weak Match"

    # ---------------- EXPLANATION METRICS ----------------
    mandatory_match_percentage = (
        (len(mandatory_skills) - len(mandatory_missing)) / len(mandatory_skills)
        if mandatory_skills else 1
    )
    # ---------------- RELIABILITY FLAG ----------------
    reliability_flag = None
    if rule_score < 0.2 and semantic_score > 0.3:
        reliability_flag = "low_keyword_overlap_possible_vocabulary_mismatch"
    elif len(job_data["skill_weights"]) < 5:
        reliability_flag = "sparse_job_description_low_confidence"

    # Filter soft skills from what is displayed to the user
    missing_required_display = [
        skill for skill in missing_required
        if skill not in SOFT_SKILLS
    ]

    matched_required_display = matched_required

    candidate_insights = generate_candidate_insights(
        {
            "semantic_score": semantic_score,
            "total_experience": experience,
            "rule_score": rule_score,
            "demonstrated_skills": categorized_skills["Demonstrated"],
            "mentioned_only_skills": categorized_skills["Mentioned Only"]
        },
        {
            "matched_skills": list(matched_required) if isinstance(matched_required, set) else matched_required,
            "missing_skills": missing_required_display
        }
    )

    return {
        "final_score": round(final_score, 4),
        "reliability_flag": reliability_flag,
        "base_score": round(base_score, 4),
        "experience_bonus": round(experience_bonus, 4),
        "pre_penalty_score": round(pre_penalty_score, 4),
        "rule_score": round(rule_score, 4),
        "semantic_score": round(semantic_score, 4),
        "matched_required": matched_required_display,
        "missing_required": missing_required_display,
        "skill_coverage": skill_coverage,
        "skill_gap_analysis": skill_gap,
        "semantic_skill_matches": semantic_skill_matches,
        "match_category": category,
        "demonstrated_skills": categorized_skills["Demonstrated"],
        "mentioned_only_skills": categorized_skills["Mentioned Only"],
        "missing_skills": categorized_skills["Not Found"],
        "semantic_evidence": semantic_evidence,
        "candidate_insights": candidate_insights,
        "skill_evidence": {**categorized_skills["Demonstrated"], **categorized_skills["Mentioned Only"]},
        "explanation": {
            "semantic_contribution": round(semantic_weight * semantic_score, 4),
            "rule_contribution": round(rule_weight * rule_score, 4),
            "experience_bonus": round(experience_bonus, 4),
            "candidate_experience_years": experience,
            "experience_source": experience_source, 
            "required_experience_years": required_experience,
            "mandatory_missing_count": len(mandatory_missing),
            "mandatory_match_percentage": round(mandatory_match_percentage, 2),
            "penalty_multiplier": round(penalty_multiplier, 4)
        }
    }