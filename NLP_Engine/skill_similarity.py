from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def are_skills_similar(skill1, skill2, threshold=0.65):
    """
    Check semantic similarity between two skills.
    Returns True if similarity >= threshold
    """

    emb1 = model.encode(skill1)
    emb2 = model.encode(skill2)

    similarity = cosine_similarity([emb1], [emb2])[0][0]

    return similarity >= threshold


def find_semantic_skill_matches(required_skills, resume_skills, threshold=0.65):
    """
    Finds semantic matches when exact skill match fails.
    """

    semantic_matches = {}

    for req_skill in required_skills:
        for res_skill in resume_skills:

            if req_skill == res_skill:
                continue

            if are_skills_similar(req_skill, res_skill, threshold):
                semantic_matches[req_skill] = res_skill

    return semantic_matches