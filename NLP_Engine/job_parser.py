import re
from NLP_Engine.skill_extractor import  normalize_skills
from NLP_Engine.job_skill_extractor import extract_job_skills, generate_skill_weights
from NLP_Engine.skill_db import ALL_SKILLS
from NLP_Engine.phase_extractor import extract_technical_phrases


# ----------------------------
# CONFIG
# ----------------------------


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
    extracted = set()

    normalized_skills = normalize_skills(ALL_SKILLS)

    for skill in normalized_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            extracted.add(skill)

    return list(extracted)


# ----------------------------
# JOB PARSER
# ----------------------------



def build_job_data(job_text: str):

    job_text_lower = job_text.lower()
    #Extract technical phrases using spacy
    phrases = extract_technical_phrases(job_text)
    sentences = re.split(r"[.\n]", job_text_lower)

    extracted_skills = set(normalize_skills(extract_skills(job_text)))
    for phrase in phrases:

    # Skip very long phrases
        if len(phrase.split()) > 4:
            continue

        extracted_skills.add(phrase)

    required_skills = set()
    preferred_skills = set()
    skill_weights = {}

    for skill in extracted_skills:

        pattern = r"\b" + re.escape(skill) + r"\b"
        frequency = len(re.findall(pattern, job_text_lower))

        # Base weight from frequency
        if frequency >= 4:
            weight = 2.7
        elif frequency >= 2:
            weight = 2.4
        else:
            weight = DEFAULT_WEIGHT

        # Sentence-level importance
        for sentence in sentences:
            if skill in sentence:

                if any(keyword in sentence for keyword in MANDATORY_KEYWORDS):
                    required_skills.add(skill)
                    weight = MANDATORY_WEIGHT

                elif any(keyword in sentence for keyword in PREFERRED_KEYWORDS):
                    preferred_skills.add(skill)
                    weight = max(weight, PREFERRED_WEIGHT)

        skill_weights[skill] = weight

    return {
        "text": job_text,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "skill_weights": skill_weights
    }