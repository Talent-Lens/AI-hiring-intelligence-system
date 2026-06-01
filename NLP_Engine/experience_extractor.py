import re


# --------------------------------------------------
# TOTAL EXPERIENCE EXTRACTION
# --------------------------------------------------

from datetime import datetime

def calculate_total_experience(text):
    import re
    from datetime import datetime

    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    text = text.replace("–", "-").replace("—", "-")

    # 1. Explicit mentions (highest priority)
    explicit_match = re.search(r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?experience", text, re.IGNORECASE)
    if explicit_match:
        try:
            return round(float(explicit_match.group(1)), 1)
        except:
            pass

    # 2. Section Filtering (Cleaning)
    # We remove sidebar distractions for better parsing
    cleaned_text = re.sub(r"\s+", " ", text)

    # 3. Enhanced Date Range Extraction
    months_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    # Simple regex for months (using non-capturing groups (?:...) to avoid unpacking errors)
    month_regex = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*|\d{1,2}"
    year_regex = r"(\d{4}|\d{2}(?=['’]))"
    
    # Pattern: (Month)? Year
    # Group 1: Month, Group 2: Year
    date_pattern = rf"(?:({month_regex})[./\-\s]*)?{year_regex}"
    
    # Range: Date to (Date or Present/Preset)
    # Group 1,2: Start Month/Year | Group 3,4: End Month/Year
    range_pattern = rf"{date_pattern}\s*(?:-|\bto\b)\s*(?:{date_pattern}|(present|current|now|preset))"
    
    matches = re.findall(range_pattern, cleaned_text, re.IGNORECASE)
    
    ranges = []
    # matches will now return (start_m, start_y, end_m, end_y, present_flag)
    for start_m_str, start_y_str, end_m_str, end_y_str, pres_flag in matches:
        try:
            def get_month(m_str):
                if not m_str: return 1
                m_str = m_str.lower()[:3]
                return months_map.get(m_str, 1) if not m_str.isdigit() else max(1, min(12, int(m_str)))

            def get_year(y_str):
                y = int(y_str)
                return y + 2000 if y < 100 else y

            start_m = get_month(start_m_str)
            start_y = get_year(start_y_str)
            
            # Handle Present/Preset
            if pres_flag or (not end_y_str and not end_m_str):
                end_m = current_month
                end_y = current_year
            else:
                end_m = get_month(end_m_str)
                end_y = get_year(end_y_str)

            start_val = start_y * 12 + start_m
            end_val = end_y * 12 + end_m
            
            if start_val < end_val:
                ranges.append((start_val, end_val))
        except:
            continue

    if not ranges:
        # Fallback to just years if months fail
        simple_years = re.findall(r"(\d{4})\s*-\s*(\d{4}|present|preset)", cleaned_text, re.IGNORECASE)
        for s, e in simple_years:
            sy = int(s)
            ey = current_year if e.lower() in ["present", "preset"] else int(e)
            if ey >= sy:
                ranges.append((sy * 12, ey * 12))

    # Merge overlapping ranges
    if not ranges:
        return 0.5
        
    ranges.sort()
    total_months = 0
    if ranges:
        curr_s, curr_e = ranges[0]
        for next_s, next_e in ranges[1:]:
            if next_s <= curr_e:
                curr_e = max(curr_e, next_e)
            else:
                total_months += (curr_e - curr_s)
                curr_s, curr_e = next_s, next_e
        total_months += (curr_e - curr_s)

    final_years = total_months / 12.0
    return round(final_years, 1) if final_years > 0 else 0.5


    
# --------------------------------------------------
# SKILL-SPECIFIC EXPERIENCE
# --------------------------------------------------

