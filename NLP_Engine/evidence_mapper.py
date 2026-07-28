
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load model (Singleton pattern for efficiency if needed, but here simple local)
# In production, we'd share this with matcher.py
from NLP_Engine.model_singleton import get_model
model = get_model()

# Cache for job embeddings
_job_evidence_cache = {}

def extract_semantic_evidence(job_text, resume_text, threshold=0.60):
    """
    Extracts resume sentences that semantically match job requirements.
    """
    # 1. Split into meaningful sentences/blocks
    # We look for lines or sentences that are at least 30 chars long
    # We also filter out lines that look like a simple list of skills (many commas)
    job_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n', job_text) if len(s.strip()) > 30]
    resume_sentences = [
    s.strip()
    for s in re.split(r'(?<=[.!?])\s+|\n', resume_text)
    if len(s.strip()) > 30 and s.count(',') < 10
]
    
    if not job_sentences or not resume_sentences:
        return []

    # 2. Encode
    # Cache job embeddings to avoid Redundant work in loops
    job_key = "\n".join(job_sentences)
    if job_key not in _job_evidence_cache:
         _job_evidence_cache[job_key] = model.encode(job_sentences, show_progress_bar=False)
    
    job_embeddings = _job_evidence_cache[job_key]
    resume_embeddings = model.encode(resume_sentences, show_progress_bar=False)
    
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

THEME_KEYWORDS = {
    "Software Development": ["python", "java", "c++", "javascript", "coding", "software", "development"],
    "Cloud & Infrastructure": ["cloud", "aws", "azure", "gcp", "devops", "docker", "kubernetes", "infrastructure"],
    "AI & Machine Learning": ["ml", "machine learning", "deep learning", "data science", "ai", "tensorflow", "pytorch", "models"],
    "NLP": ["nlp", "text", "bert", "gpt", "language", "semantic"],
    "Frontend Development": ["frontend", "react", "angular", "vue", "html", "css", "ui", "ux"],
    "Backend Development": ["backend", "sql", "database", "api", "rest", "microservices", "flask", "django", "node"],
    "Project Methodology": ["agile", "scrum", "project management", "workflow"],
    "Marketing & Growth": ["marketing", "seo", "sem", "content", "brand", "campaign", "analytics"],
    "Finance & Accounting": ["financial", "accounting", "budget", "forecast", "valuation", "gaap"],
    "Sales & Business Development": ["sales", "revenue", "pipeline", "account", "negotiation", "crm"],
    "Product Management": ["product", "roadmap", "backlog", "okr", "user story", "go-to-market"],
    "Design & UX": ["design", "figma", "ux", "ui", "wireframe", "prototype", "user research"],
    "HR & People": ["recruitment", "talent", "onboarding", "performance", "hris", "compensation"],
    "Operations & Supply Chain": ["operations", "supply chain", "logistics", "procurement", "lean"],
    "Leadership & Management": ["leadership", "management", "lead", "coordinate", "mentor", "team"],
    "Data & Analytics": ["data", "sql", "analytics", "dashboard", "reporting", "tableau", "power bi"],
}

def generate_reason(job_requirement):
    job_lower = job_requirement.lower()
    themes = [name for name, keywords in THEME_KEYWORDS.items()
              if any(kw in job_lower for kw in keywords)]
    unique_themes = list(dict.fromkeys(themes))[:2]
    if unique_themes:
        theme_str = " and ".join(unique_themes)
        return f"Strong alignment with {theme_str} requirements."
    return "Relevant experience aligned with the professional requirements of this role."