from NLP_Engine.skill_extractor import extract_skills, normalize_skills
from NLP_Engine.advanced_skill_extractor import extract_additional_skills


def extract_job_skills(job_text):
     # Extract skills using phrase matcher
    base_skills = extract_skills(job_text)

    # Extract additional tech tokens
    extra_skills = extract_additional_skills(job_text)

    # Combine both lists
    combined = set(base_skills).union(set(extra_skills))

    skills = normalize_skills(combined)
    
    return skills


def generate_skill_weights(skills):
    
    skills = normalize_skills(skills)

    skill_weights = {}

    for skill in skills:

        # Default weight
        weight = 2

        # Critical technologies
        if skill in ["python", "aws", "pytorch", "sql"]:
            weight = 3

        # Core ML skills
        elif skill in ["machine learning", "deep learning", "natural language processing"]:
            weight = 2

        skill_weights[skill] = weight

    return skill_weights