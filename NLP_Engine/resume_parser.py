import os
from NLP_Engine.utils import extract_text_from_pdf, clean_text
from NLP_Engine.skill_extractor import extract_skills

def parse_resume(path: str):
    if path.endswith(".pdf"):
        text = extract_text_from_pdf(path)
    else:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    text = clean_text(text)
    skills = extract_skills(text)

    return {
        "text": text,
        "skills": skills
    }