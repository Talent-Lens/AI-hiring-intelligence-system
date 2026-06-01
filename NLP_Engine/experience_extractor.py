import re


# --------------------------------------------------
# TOTAL EXPERIENCE EXTRACTION
# --------------------------------------------------

from datetime import datetime

def calculate_total_experience(text):
    import re
    from datetime import datetime

    current_year = datetime.now().year

    text = text.replace("–", "-").replace("—", "-")

    # --- Extract only Work Experience section ---
    work_section = ""

    work_match = re.search(
        r"(work experience|professional experience|employment history|internships?|experience)(.*?)(education|projects|skills|certifications|references|extracurricular|training|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if work_match:
        work_section = work_match.group(2)
    else:
        # fallback if no section found
        work_section = text

    pattern = r"(\d{4})\s*-\s*(\d{4}|present|Present)"
    matches = re.findall(pattern, work_section)

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

