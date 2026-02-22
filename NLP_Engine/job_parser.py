import re

# You can later move this to skill_extractor.py or a config file
MASTER_SKILLS = [
    "python", "java", "c++", "machine learning", "deep learning",
    "nlp", "sql", "mongodb", "react", "node.js", "django",
    "flask", "tensorflow", "pytorch", "aws", "docker",
    "kubernetes", "git", "linux"
]


def extract_skills(text):
    text = text.lower()
    extracted = []

    for skill in MASTER_SKILLS:
        if skill.lower() in text:
            extracted.append(skill)

    return list(set(extracted))


def parse_job_description(job_path):
    with open(job_path, "r", encoding="utf-8") as f:
        text = f.read()

    text_lower = text.lower()

    # Basic rule-based separation
    required_section = ""
    preferred_section = ""

    required_match = re.search(r"(required skills:)(.*?)(preferred skills:|$)", text_lower, re.DOTALL)
    preferred_match = re.search(r"(preferred skills:)(.*)", text_lower, re.DOTALL)

    if required_match:
        required_section = required_match.group(2)

    if preferred_match:
        preferred_section = preferred_match.group(2)

    required_skills = extract_skills(required_section if required_section else text_lower)
    if not required_skills:
        required_skills = extract_skills(text_lower)

    preferred_skills = extract_skills(preferred_section)
    
    return {
        "text": text_lower,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills
    }