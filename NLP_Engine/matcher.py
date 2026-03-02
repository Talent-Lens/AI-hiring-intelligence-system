from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load model once (very important)
model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_semantic_score(job_text, resume_text):
    job_embedding = model.encode([job_text])
    resume_embedding = model.encode([resume_text])

    similarity = cosine_similarity(job_embedding, resume_embedding)[0][0]
    return float(similarity)


def compute_rule_score(required_skills, resume_skills, skill_weights):
    if not required_skills:
        return 0.0, [], []

    matched_required = required_skills.intersection(resume_skills)
    missing_required = required_skills.difference(resume_skills)

    total_weight = sum(skill_weights.get(skill, 1) for skill in required_skills)
    matched_weight = sum(skill_weights.get(skill, 1) for skill in matched_required)

    rule_score = matched_weight / total_weight if total_weight > 0 else 0

    return rule_score, list(matched_required), list(missing_required)

def match_resume_to_job(job_data, resume_data, semantic_weight=0.6, rule_weight=0.4):
    job_text = job_data["text"]
    required_skills = job_data["required_skills"]

    resume_text = resume_data["text"]
    resume_skills = resume_data["skills"]

    # 1️⃣ Rule-based score
    rule_score, matched_required, missing_required = compute_rule_score(
        required_skills,
        resume_skills,
        job_data["skill_weights"]
    )

    # 2️⃣ Semantic score
    semantic_score = compute_semantic_score(job_text, resume_text)

    # 3️⃣ Hybrid final score
    final_score = (semantic_weight * semantic_score) + (rule_weight * rule_score)
    # -------- Mandatory Skill Penalty --------

    mandatory_missing = [
        skill for skill in missing_required
        if job_data["skill_weights"].get(skill, 0) == 3
]
    total_mandatory = [
        skill for skill, weight in job_data["skill_weights"].items()
        if weight == 3
]

    if total_mandatory:
        penalty_ratio = len(mandatory_missing) / len(total_mandatory)
        final_score *= (1 - 0.5 * penalty_ratio)
    

    return {
        "final_score": round(final_score, 4),
        "rule_score": round(rule_score, 4),
        "semantic_score": round(semantic_score, 4),
        "matched_required": matched_required,
        "missing_required": missing_required
    }