import re

# ----------------------------
# CONFIG
# ----------------------------

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

MANDATORY_KEYWORDS = ["must", "required", "mandatory", "essential"]
PREFERRED_KEYWORDS = ["preferred", "nice to have", "plus"]

DEFAULT_WEIGHT = 2
MANDATORY_WEIGHT = 3
PREFERRED_WEIGHT = 1


# ----------------------------
# SKILL EXTRACTION
# ----------------------------

def extract_skills(text: str):
    text = text.lower()
    extracted = []

    for skill in MASTER_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            extracted.append(skill)

    return extracted


# ----------------------------
# JOB PARSER
# ----------------------------

def build_job_data(job_text: str):
    job_text_lower = job_text.lower()
    sentences = re.split(r"[.\n]", job_text_lower)

    required_skills = set()
    skill_weights = {}

    for skill in MASTER_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        frequency = len(re.findall(pattern, job_text_lower))

        if frequency == 0:
            continue

        required_skills.add(skill)

        # Base weight from frequency
        if frequency >= 4:
            weight = 2.7
        elif frequency >= 2:
            weight = 2.4
        else:
            weight = DEFAULT_WEIGHT

        # Check sentence-level importance override
        for sentence in sentences:
            if skill in sentence:
                if any(keyword in sentence for keyword in MANDATORY_KEYWORDS):
                    weight = MANDATORY_WEIGHT
                elif any(keyword in sentence for keyword in PREFERRED_KEYWORDS):
                    weight = max(weight, PREFERRED_WEIGHT)

        skill_weights[skill] = weight

    return {
        "text": job_text,
        "required_skills": required_skills,
        "skill_weights": skill_weights
    }