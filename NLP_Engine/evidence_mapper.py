from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load model (Singleton pattern for efficiency if needed, but here simple local)
# In production, we'd share this with matcher.py
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_semantic_evidence(job_text, resume_text, threshold=0.60):
    """
    Extracts resume sentences that semantically match job requirements.
    """
    # 1. Split into meaningful sentences/blocks
    # We look for lines or sentences that are at least 30 chars long
    # We also filter out lines that look like a simple list of skills (many commas)
    job_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n', job_text) if len(s.strip()) > 30]
    resume_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n', resume_text) 
                        if len(s.strip()) > 30 and s.count(',') < 5]
    
    if not job_sentences or not resume_sentences:
        return []

    # 2. Encode
    job_embeddings = model.encode(job_sentences)
    resume_embeddings = model.encode(resume_sentences)
    
    # 3. Compute Similarity matrix (Resume x Job)
    similarities = cosine_similarity(resume_embeddings, job_embeddings)
    
    evidence_mappings = []
    used_resume_indices = set()
    
    # We want to find the best resume sentence for each job requirement
    for j_idx, job_sent in enumerate(job_sentences):
        # Only look at sentences that look likerequirements (not headers)
        if job_sent.isupper() or len(job_sent) < 40:
            continue
            
        best_r_idx = similarities[:, j_idx].argmax()
        score = similarities[best_r_idx, j_idx]
        
        if score >= threshold and best_r_idx not in used_resume_indices:
            used_resume_indices.add(best_r_idx)
            
            reason = generate_reason(job_sent)
            
            evidence_mappings.append({
                "resume_evidence": resume_sentences[best_r_idx],
                "job_requirement": job_sent,
                "reason": reason,
                "score": float(score)
            })
            
    # Sort by score and take top 5 most impactful matches
    evidence_mappings.sort(key=lambda x: x["score"], reverse=True)
    return evidence_mappings[:5]

def generate_reason(job_requirement):
    """
    Generates a human-friendly reason for the semantic match.
    """
    job_lower = job_requirement.lower()
    themes = []
    
    if any(kw in job_lower for kw in ["python", "java", "c++", "javascript", "coding", "software", "development"]):
        themes.append("Software Development")
    if any(kw in job_lower for kw in ["cloud", "aws", "azure", "gcp", "devops", "docker", "kubernetes", "infrastructure"]):
        themes.append("Cloud & Infrastructure")
    if any(kw in job_lower for kw in ["ml", "machine learning", "deep learning", "data science", "ai", "tensorflow", "pytorch", "models"]):
        themes.append("AI & Machine Learning")
    if any(kw in job_lower for kw in ["nlp", "text", "bert", "gpt", "language", "semantic"]):
        themes.append("NLP")
    if any(kw in job_lower for kw in ["frontend", "react", "angular", "vue", "html", "css", "ui", "ux"]):
        themes.append("Frontend Development")
    if any(kw in job_lower for kw in ["backend", "sql", "database", "api", "rest", "microservices", "flask", "django", "node"]):
        themes.append("Backend Development")
    if any(kw in job_lower for kw in ["leadership", "management", "lead", "coordinate", "mentor", "team"]):
        themes.append("Leadership & Team Management")
    if any(kw in job_lower for kw in ["agile", "scrum", "project management", "workflow"]):
        themes.append("Project Methodology")

    if themes:
        # Take unique themes and join
        unique_themes = []
        for t in themes:
            if t not in unique_themes: unique_themes.append(t)
        
        if len(unique_themes) > 2:
            theme_str = ", ".join(unique_themes[:2]) + " and related"
        else:
            theme_str = " and ".join(unique_themes)
            
        return f"Strong alignment with {theme_str} requirements."
    
    return "Relevant experience for the professional requirements specified in the role."
