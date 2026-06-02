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

    # Normalize separators
    text = text.replace("–", "-").replace("—", "-")

    # 1. Section Identification
    # We look for major headers to split the text. 
    # Since the text is often flattened (newlines removed), we rely on keywords.
    headers = [
        ("EXP", r"\b(WORK EXPERIENCE|EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY)\b"),
        ("EDU", r"\b(EDUCATION|ACADEMIC BACKGROUND|SCHOLASTIC)\b"),
        ("PROJECTS", r"\b(PROJECTS|PERSONAL PROJECTS)\b"),
        ("SKILLS", r"\b(SKILLS|TECHNICAL SKILLS)\b"),
        ("SUMMARY", r"\b(SUMMARY|OBJECTIVE|ABOUT ME)\b")
    ]
    
    found_headers = []
    for tag, pattern in headers:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            found_headers.append((m.start(), tag))
            
    found_headers.sort()
    
    segments = []
    if not found_headers:
        segments.append(("UNKNOWN", text))
    else:
        # Before first header
        if found_headers[0][0] > 0:
            segments.append(("HEADERless", text[:found_headers[0][0]]))
        # Between headers
        for i in range(len(found_headers)):
            start_idx = found_headers[i][0]
            tag = found_headers[i][1]
            end_idx = found_headers[i+1][0] if i+1 < len(found_headers) else len(text)
            segments.append((tag, text[start_idx:end_idx]))
            
    # 2. Date Range Extraction logic
    months_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    month_regex = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*|\d{1,2}"
    year_regex = r"(\d{4}|\d{2}(?=['’]))"
    date_pattern = rf"(?:({month_regex})[./\-\s]*)?{year_regex}"
    range_pattern = rf"{date_pattern}\s*(?:-|\bto\b)\s*(?:{date_pattern}|(present|current|now|preset))"
    
    ranges = []
    
    for tag, seg_text in segments:
        # Exclude EDUCATION section entirely
        if tag == "EDU":
            continue
            
        matches = re.findall(range_pattern, seg_text, re.IGNORECASE)
        
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

    # 3. Explicit mentions (used as floor/sanity check)
    explicit_match = re.search(r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?experience", text, re.IGNORECASE)
    explicit_val = 0
    if explicit_match:
        try:
            explicit_val = float(explicit_match.group(1))
        except:
            pass

    if not ranges:
        return round(explicit_val, 1) if explicit_val > 0 else 0.5
        
    # Merge overlapping ranges
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
    calculated_val = round(final_years, 1)
    
    # Take max of calculated and explicit (but if explicit is suspiciously high, we might want to cap it. 
    # For now, max is safer to avoid penalizing users with hidden/undocumented experience).
    result = max(calculated_val, explicit_val)
    
    return round(result, 1) if result > 0 else 0.5


    
# --------------------------------------------------
# SKILL-SPECIFIC EXPERIENCE
# --------------------------------------------------

