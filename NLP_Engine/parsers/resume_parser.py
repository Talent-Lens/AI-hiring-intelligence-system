
from NLP_Engine.advanced_skill_extractor import extract_additional_skills
from NLP_Engine.skill_extractor import extract_skills, normalize_skills
from NLP_Engine.utils import extract_text_from_pdf
from NLP_Engine.experience_extractor import calculate_total_experience



def parse_resume(file_path: str, required_skills):

    text = extract_text_from_pdf(file_path)
    
    # 1. Extract skills with evidence
    skill_evidence = extract_skills(text, include_evidence=True)
    extra_evidence = extract_additional_skills(text, include_evidence=True)
    
    # Merge evidence
    for skill, evidence in extra_evidence.items():
        if skill not in skill_evidence or len(evidence) > len(skill_evidence[skill]):
            skill_evidence[skill] = evidence

    # 2. Get normalized set for backward compatibility
    skills = set(skill_evidence.keys())
    skills = set(normalize_skills(skills))
    
    total_experience = calculate_total_experience(text)

    return {
        "text": text,
        "skills": list(skills),
        "skill_evidence": skill_evidence,
        "total_experience": total_experience,
    }