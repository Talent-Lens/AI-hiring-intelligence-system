from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(resume_text, job_text):
    resume_embedding = model.encode(resume_text)
    job_embedding = model.encode(job_text)

    similarity = cosine_similarity(
        [resume_embedding],
        [job_embedding]
    )[0][0]

    return round(float(similarity), 4)


def calculate_hybrid_score(
    resume_text,
    job_text,
    resume_skills,
    required_skills,
    preferred_skills
):
    # Rule section
    resume_set = set(resume_skills)
    required_set = set(required_skills)
    preferred_set = set(preferred_skills)

    required_matches = resume_set & required_set
    preferred_matches = resume_set & preferred_set

    required_missing = required_set - resume_set
    preferred_missing = preferred_set - resume_set

    required_score = (len(required_matches) / len(required_set)) if required_set else 0
    preferred_score = (len(preferred_matches) / len(preferred_set)) if preferred_set else 0

    rule_score = (0.7 * required_score) + (0.3 * preferred_score)

    # Semantic section
    semantic_score = calculate_semantic_similarity(resume_text, job_text)

    # Hybrid
    final_score = (0.6 * semantic_score) + (0.4 * rule_score)

    return {
        "final_score": round(final_score, 4),
        "semantic_score": semantic_score,
        "rule_score": round(rule_score, 4),
        "matched_required_skills": list(required_matches),
        "matched_preferred_skills": list(preferred_matches),
        "missing_required_skills": list(required_missing),
        "missing_preferred_skills": list(preferred_missing)
    }