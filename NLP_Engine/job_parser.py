import re
from NLP_Engine.skill_extractor import extract_skills


REQUIRED_KEYWORDS = [
    "required",
    "must have",
    "must-have",
    "requirements",
    "mandatory",
    "essential"
]
SKILL_WEIGHTS = {
    "python": 3,
    "machine learning": 3,
    "sql": 2,
    "aws": 2,
    "docker": 1,
    "git": 1
}


def parse_job_description(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    lower_text = text.lower()

    # 1️⃣ Extract all skills from entire job description
    all_skills = extract_skills(text)

    required_skills = set()

    # 2️⃣ Try to detect required sections
    for keyword in REQUIRED_KEYWORDS:
        pattern = keyword + r"(.*?)(\n\n|$)"
        matches = re.findall(pattern, lower_text, re.DOTALL)

        for match in matches:
            section_text = match[0]
            required_skills.update(extract_skills(section_text))

    # 3️⃣ Fallback if no required section detected
    if not required_skills:
        required_skills = all_skills

    return {
        "text": text,
        "all_skills": all_skills,
        "required_skills": required_skills,
        "skill_weights":SKILL_WEIGHTS
    }