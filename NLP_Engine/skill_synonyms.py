SKILL_SYNONYMS = {

    "machine learning": [
        "ml",
        "machine-learning",
        "machine learning models"
    ],

    "natural language processing": [
        "nlp",
        "text processing",
        "language models"
    ],

    "python": [
        "python3",
        "py"
    ],

    "sql": [
        "mysql",
        "postgresql",
        "sqlite",
        "database querying"
    ],

    "pytorch": [
        "torch",
        "pytorch framework"
    ],

    "aws": [
        "amazon web services",
        "aws cloud"
    ]

}
def normalize_skills(extracted_skills):

    normalized = set()

    for skill in extracted_skills:
        skill = skill.lower()

        found = False

        for canonical, synonyms in SKILL_SYNONYMS.items():

            if skill == canonical or skill in synonyms:
                normalized.add(canonical)
                found = True
                break

        if not found:
            normalized.add(skill)

    return list(normalized)