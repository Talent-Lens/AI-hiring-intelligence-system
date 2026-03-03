import re


# --------------------------------------------------
# TOTAL EXPERIENCE EXTRACTION
# --------------------------------------------------

from datetime import datetime


MONTH_MAP = {
    "january": 1, "february": 2, "march": 3,
    "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9,
    "october": 10, "november": 11, "december": 12
}
def calculate_total_experience(text):
    current_year = datetime.now().year
    
    # Normalize different dash types to standard hyphen
    text = text.replace("–", "-").replace("—", "-")
    
    # Match patterns like: 2015 - 2020 OR 2015 - Present
    pattern = r"(\d{4})\s*-\s*(\d{4}|present|Present)"
    matches = re.findall(pattern, text)

    total_years = 0

    for start, end in matches:
        start_year = int(start)

        if end.lower() == "present":
            end_year = current_year
        else:
            end_year = int(end)

        if end_year >= start_year:
            total_years += (end_year - start_year)

    return round(total_years, 1) if total_years > 0 else 0.1


    
# --------------------------------------------------
# SKILL-SPECIFIC EXPERIENCE
# --------------------------------------------------

def extract_skill_experience(text: str, required_skills):
    """
    Extracts experience duration for required skills only.
    Returns dict: {skill: years}
    """

    skill_experience = {}
    text_lower = text.lower()

    for skill in required_skills:
        pattern = rf'(\d+)\+?\s*(?:years?|yrs?).{{0,20}}{re.escape(skill)}'
        matches = re.findall(pattern, text_lower)

        if matches:
            years = [int(m) for m in matches]
            skill_experience[skill] = max(years)

    return skill_experience