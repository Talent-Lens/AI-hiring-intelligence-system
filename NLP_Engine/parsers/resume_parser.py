from NLP_Engine.skill_extractor import extract_skills
from NLP_Engine.utils import extract_text_from_pdf


def parse_resume(file_path: str):
    """
    Parses a resume PDF and returns structured data.
    """

    # Extract text from PDF
    text = extract_text_from_pdf(file_path)

    # Extract normalized skills
    skills = set(extract_skills(text))

    return {
        "text": text,
        "skills": skills
    }