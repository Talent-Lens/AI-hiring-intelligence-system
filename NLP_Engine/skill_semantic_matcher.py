from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load once (global model)
model = SentenceTransformer("all-MiniLM-L6-v2")

#cache for skill embeddings
skill_embedding_cache = {}

def get_skill_embedding(skill):

    if skill in skill_embedding_cache:
        return skill_embedding_cache[skill]

    embedding = model.encode(skill, convert_to_tensor=False)
    skill_embedding_cache[skill] = embedding

    return embedding


def find_semantic_skill_matches(required_skills, resume_skills, threshold=0.75):
    """
    Finds semantically similar skills between job and resume
    using sentence embeddings.
    """

    matches = {}

    required_list = list(required_skills)
    resume_list = list(resume_skills)

    if len(required_list) == 0 or len(resume_list) == 0:
        return matches

    required_list = list(required_skills)
    resume_list = list(resume_skills)

    # Encode skills
    import numpy as np

    req_embeddings = np.array([get_skill_embedding(skill) for skill in required_list])
    res_embeddings = np.array([get_skill_embedding(skill) for skill in resume_list])
    
    # Compute similarity matrix
    similarity_matrix = cosine_similarity(req_embeddings, res_embeddings)
    used_resume_indices = set()

    for i, req_skill in enumerate(required_list):
        best_match_index = similarity_matrix[i].argmax()
        best_score = similarity_matrix[i][best_match_index]
        
        #Prevent same resume skill used twice
        if best_match_index in used_resume_indices:
            continue

        if best_score >= threshold:
            matches[req_skill] = resume_list[best_match_index]
            used_resume_indices.add(best_match_index)

    return matches