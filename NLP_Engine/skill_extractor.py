skill_list = [
    "python", "java", "javascript", "react", "nodejs",
    "sql", "mongodb", "docker", "aws", "spring"
]

skill_aliases = {
    "node.js": "nodejs",
    "node js": "nodejs",
    "react js": "react",
    "mongo db": "mongodb",
}


def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
    return skill_aliases.get(skill, skill)


def extract_skills(text: str):
    text = text.lower()
    found_skills = set()

    for skill in skill_list:
        if skill in text:
            normalized = normalize_skill(skill)
            found_skills.add(normalized)

    return list(found_skills)