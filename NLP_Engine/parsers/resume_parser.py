from NLP_Engine.skill_extractor import extract_skills


def parse_resume(file_path):
    """
    Reads resume text file and extracts skills.
    Returns structured dictionary used by matcher.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    skills = extract_skills(text)

    return {
        "text": text,
        "skills": skills
    }