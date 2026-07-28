# advanced_skill_extractor.py
import re
from NLP_Engine.skill_db import ALL_SKILLS

def extract_additional_skills(text: str, include_evidence: bool = False):
    text_lower = text.lower()
    skill_evidence = {}
    lines = [l.strip() for l in text.split('\n') if l.strip()]

    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            best_line = next(
                (l for l in lines if re.search(pattern, l.lower())), skill
            )
            if include_evidence:
                skill_evidence[skill] = best_line
            else:
                skill_evidence[skill] = True

    return skill_evidence if include_evidence else set(skill_evidence.keys())