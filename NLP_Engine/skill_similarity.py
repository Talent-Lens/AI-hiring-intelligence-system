from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from NLP_Engine.model_singleton import get_model

# Load embedding model
model = get_model()


# Cache for skill embeddings
_skill_cache = {}

def are_skills_similar(skill1, skill2, threshold=0.65):
    """
    Check semantic similarity between two skills.
    Returns True if similarity >= threshold
    """
    if skill1 not in _skill_cache:
        _skill_cache[skill1] = model.encode(skill1, show_progress_bar=False)
    if skill2 not in _skill_cache:
        _skill_cache[skill2] = model.encode(skill2, show_progress_bar=False)

    emb1 = _skill_cache[skill1]
    emb2 = _skill_cache[skill2]

    similarity = cosine_similarity([emb1], [emb2])[0][0]

    return similarity >= threshold


SEMANTIC_MATCH_BLACKLIST = {("sql", "sap"), ("sales", "scala"), ("r", "c"), ("go", "c")}

def find_semantic_skill_matches(required_skills, resume_skills, threshold=0.70):  # raise to 0.70
    semantic_matches = {}
    for req_skill in required_skills:
        if len(req_skill) < 4:  # skip very short tokens — too noisy
            continue
        for res_skill in resume_skills:
            if req_skill == res_skill or len(res_skill) < 4:
                continue
            pair = tuple(sorted([req_skill, res_skill]))
            if pair in SEMANTIC_MATCH_BLACKLIST:
                continue
            if are_skills_similar(req_skill, res_skill, threshold):
                semantic_matches[req_skill] = res_skill
    return semantic_matches