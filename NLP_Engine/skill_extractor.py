import re


# Canonical skills
MASTER_SKILLS = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "nlp",
    "sql",
    "mongodb",
    "react",
    "node.js",
    "django",
    "flask",
    "tensorflow",
    "pytorch",
    "aws",
    "docker",
    "kubernetes",
    "git"
]


# Alias mapping (variation → canonical)
SKILL_ALIASES = {
    "ml": "machine learning",
    "natural language processing": "nlp",
    "nodejs": "node.js",
    "amazon web services": "aws",
    "k8s": "kubernetes"
}


def normalize_text(text):
    return text.lower()


def extract_skills(text):
    text = normalize_text(text)
    found_skills = set()

    # 1️⃣ Detect canonical skills
    for skill in MASTER_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    # 2️⃣ Detect aliases and convert to canonical
    for alias, canonical in SKILL_ALIASES.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, text):
            found_skills.add(canonical)

    return found_skills