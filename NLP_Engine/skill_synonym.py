SKILL_SYNONYMS = {
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",

    "ml": "machine learning",
    "machine learning": "machine learning",

    "torch": "pytorch",
    "pytorch": "pytorch",

    "amazon web services": "aws",
    "aws": "aws",

    "structured query language": "sql",
    "sql": "sql"
}
def normalize_skills(skill_list):
    normalized = []

    for skill in skill_list:
        s = skill.lower().strip()

        if s in SKILL_SYNONYMS:
            normalized.append(SKILL_SYNONYMS[s])
        else:
            normalized.append(s)

    return normalized