from pydoc import text
from NLP_Engine.skill_extractor import extract_skills
from NLP_Engine.utils import extract_text_from_pdf
from NLP_Engine.experience_extractor import (
    calculate_total_experience,
    extract_skill_experience
)


def parse_resume(file_path: str, required_skills=None):

    text = extract_text_from_pdf(file_path)
    skills = set(extract_skills(text))
    total_experience = calculate_total_experience(text)

    skill_experience = {}
    if required_skills:
        skill_experience = extract_skill_experience(text, required_skills)
        
   
    return {
        "text": text,
        "skills": skills,
        "total_experience": total_experience,
        "skill_experience": skill_experience
    }