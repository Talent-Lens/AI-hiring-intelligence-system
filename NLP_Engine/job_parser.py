from NLP_Engine.utils import clean_text
from NLP_Engine.skill_extractor import extract_skills


def parse_job_description(path: str):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    text = clean_text(text)
    skills = extract_skills(text)

    return {
        "text": text,
        "skills": skills
    }