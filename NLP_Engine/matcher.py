from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from NLP_Engine.skill_gap_analyzer import analyze_skill_gap
from NLP_Engine.skill_synonyms import normalize_skills
from NLP_Engine.skill_similarity import find_semantic_skill_matches

# ----------------------------
# LOAD MODEL (Singleton)
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# ----------------------------
# SEMANTIC SCORE
# ----------------------------
def compute_semantic_score(job_text, resume_text):
    job_embedding = model.encode(job_text, convert_to_tensor=False)
    resume_embedding = model.encode(resume_text, convert_to_tensor=False)

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
        return 0.0, [], []

    matched_required = list(required_skills.intersection(resume_skills))
    missing_required = list(required_skills.difference(resume_skills))
    
    # ---------------- SEMANTIC SKILL MATCH ----------------

    semantic_skill_matches = find_semantic_skill_matches(
        missing_required,
        resume_skills
)

    for req_skill, res_skill in semantic_skill_matches.items():
        matched_required.append(req_skill)
        if req_skill in missing_required:
            missing_required.remove(req_skill)

    total_weight = sum(skill_weights.get(skill, 1) for skill in required_skills)

    if total_weight == 0:
        return 0.0, list(matched_required), list(missing_required)

    matched_weight = sum(skill_weights.get(skill, 1) for skill in matched_required)

    rule_score = matched_weight / total_weight

    return rule_score, list(matched_required), list(missing_required),semantic_skill_matches


# ----------------------------
# MATCH FUNCTION
# ----------------------------
def match_resume_to_job(
    job_data,
    resume_data,
    semantic_weight=0.4,
    rule_weight=0.6
):

    # Safety check
    if round(semantic_weight + rule_weight, 2) != 1.0:
        raise ValueError("semantic_weight + rule_weight must equal 1.0")

    job_text = job_data["text"]
    required_skills = set(normalize_skills(job_data["required_skills"]))

    resume_text = resume_data["text"]
    resume_skills = set(normalize_skills(resume_data["skills"]))

    
    # 1️⃣ Rule Score
    rule_score, matched_required, missing_required, semantic_skill_matches= compute_rule_score(
        required_skills,
        resume_skills,
        job_data["skill_weights"]
    )
    skill_gap = analyze_skill_gap(job_data, resume_data)

    
    # 2️⃣ Semantic Score
    semantic_score = compute_semantic_score(job_text, resume_text)

    # 3️⃣ Hybrid Base Score
    base_score = (semantic_weight * semantic_score) + \
                 (rule_weight * rule_score)

    # ---------------- EXPERIENCE BONUS ----------------
    experience = resume_data.get("total_experience", 0)
    experience_bonus = min(experience * 0.01, 0.15)

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

    # ✅ Mandatory Match Bonus
    if mandatory_skills and len(mandatory_missing) == 0:
        pre_penalty_score += 0.05

    # ---------------- TIERED PENALTY SYSTEM ----------------
    penalty_multiplier = 1.0

    if mandatory_skills:
        penalty_ratio = len(mandatory_missing) / len(mandatory_skills)

        if penalty_ratio >= 0.75:
            penalty_multiplier = 0.4   # Almost reject
        elif penalty_ratio >= 0.5:
            penalty_multiplier = 0.6  # Strong penalty
        elif penalty_ratio > 0:
            penalty_multiplier = 0.8   # Mild penalty

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

    return {
        "final_score": round(final_score, 4),
        "base_score": round(base_score, 4),
        "experience_bonus": round(experience_bonus, 4),
        "pre_penalty_score": round(pre_penalty_score, 4),
        "rule_score": round(rule_score, 4),
        "semantic_score": round(semantic_score, 4),
        "matched_required": matched_required,
        "missing_required": missing_required,
        "skill_gap_analysis": skill_gap,
        "semantic_skill_matches": semantic_skill_matches,
        "match_category": category,
        "explanation": {
            "semantic_contribution": round(semantic_weight * semantic_score, 4),
            "rule_contribution": round(rule_weight * rule_score, 4),
            "experience_bonus": round(experience_bonus, 4),
            "mandatory_missing_count": len(mandatory_missing),
            "mandatory_match_percentage": round(mandatory_match_percentage, 2),
            "penalty_multiplier": round(penalty_multiplier, 4)
        }
    }