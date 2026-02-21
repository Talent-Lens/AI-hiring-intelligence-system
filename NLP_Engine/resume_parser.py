from NLP_Engine.utils import extract_text_from_pdf, clean_text
from NLP_Engine.skill_extractor import extract_skills


def parse_resume(path: str):
    text = extract_text_from_pdf(path)
    text = clean_text(text)
    skills = extract_skills(text)

    return {
        "text": text,
        "skills": skills
    }