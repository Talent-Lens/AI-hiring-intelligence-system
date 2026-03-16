import re
from NLP_Engine.skill_extractor import  normalize_skills
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

BLACKLIST_SKILLS = {
    "experience",
    "year",
    "years",
    "knowledge",
    "skills",
    "ability",
    "abilities",
    "responsibilities",
    "responsible",
    "work",
    "job",
    "role",
    "project",
    "team",
    "projects",
    "working",
    "preferred",
    "required",
}
# ----------------------------
# SKILL EXTRACTION
# ----------------------------

def clean_job_text(text: str):

    text = text.lower()
    text = text.replace(","," ")
    text = text.replace("/"," ")
    text = text.replace("("," ")
    text = text.replace(")"," ")

    STOP_PHRASES = [
        "strong experience",
        "experience in",
        "experience with",
        "knowledge of",
        "understanding of",
        "familiar with"
    ]

    REMOVE_WORDS = [
        "preferred",
        "required",
        "must",
        "should",
        "nice to have"
    ]

    for phrase in STOP_PHRASES:
        text = text.replace(phrase, "")

    for word in REMOVE_WORDS:
        text = text.replace(word, "")

    return text

def extract_skills(text: str):
    text = text.lower()
    extracted = set()

    normalized_skills = sorted(normalize_skills(ALL_SKILLS), key=len, reverse=True)

    for skill in normalized_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            extracted.add(skill)
    
    # Remove blacklisted terms
    extracted = {
        skill for skill in extracted
        if skill not in BLACKLIST_SKILLS
    }        

    return list(extracted)



# ----------------------------
# JOB PARSER
# ----------------------------



def build_job_data(job_text: str):

    job_text_clean = clean_job_text(job_text)
    job_text_lower = job_text_clean.lower()
    #Extract technical phrases using spacy
    phrases = extract_technical_phrases(job_text_clean)
    sentences = re.split(r"[.\n]", job_text_lower)

    extracted_skills = set(extract_skills(job_text_clean))
    for phrase in phrases:
        
        words = phrase.split()

    # Skip very long phrases
        if len(words) > 2:
            continue
        if any(word in BLACKLIST_SKILLS for word in words):
            continue
        # count how many known skills appear
        skill_count = sum(1 for skill in ALL_SKILLS if skill in phrase)
        if skill_count >= 1:
            continue
        if skill_count == 0:
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