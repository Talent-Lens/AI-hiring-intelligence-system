import re
from datetime import datetime

def calculate_total_experience(text):
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    text = text.replace("–", "-").replace("—", "-")

    # 1. Explicit mentions (highest priority in OLD code)
    # We will MOVE this to a lower priority or use as a sanity check
    explicit_match = re.search(r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?experience", text, re.IGNORECASE)
    explicit_val = None
    if explicit_match:
        try:
            explicit_val = round(float(explicit_match.group(1)), 1)
        except:
            pass

    # 2. Section Filtering
    # Instead of just blob, let's try to identify sections
    # Since clean_text removes newlines, we work with a space-separated blob
    
    # Let's try to remove Education block
    # We can identify where Education starts
    edu_keywords = ["EDUCATION", "ACADEMIC BACKGROUND", "SCHOLASTIC"]
    lower_text = text.lower()
    
    # Simple strategy: find indices of major headers
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
    
    # Break text into segments
    segments = []
    for i in range(len(found_headers)):
        start_idx = found_headers[i][0]
        tag = found_headers[i][1]
        end_idx = found_headers[i+1][0] if i+1 < len(found_headers) else len(text)
        segments.append((tag, text[start_idx:end_idx]))
        
    # If no headers found, treat the whole thing as potentially Experience
    if not segments:
        segments = [("UNKNOWN", text)]
        
    # 3. Enhanced Date Range Extraction on Experience segments
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
        # Only process EXPERIENCE or UNKNOWN or PROJECTS maybe?
        # Usually we want to exclude EDUCATION at least.
        if tag == "EDU":
            continue
            
        print(f"DEBUG: Processing segment {tag}")
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
                    print(f"DEBUG: Found range {start_y}/{start_m} to {end_y}/{end_m}")
            except:
                continue

    if not ranges:
        return explicit_val if explicit_val else 0.5
        
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
    
    # Combine with explicit val
    if explicit_val and explicit_val > calculated_val:
        # If explicit is much higher, maybe we missed something. 
        # But if it's close, trust the calculated one?
        # Let's take the max but maybe cap it?
        # A common heuristic is to take the max of both if they are reasonably close.
        # But if calculated is 0, we definitely want explicit.
        return max(calculated_val, explicit_val)
    
    return calculated_val if calculated_val > 0 else 0.5

# Test Cases
test_atticus = "WORK EXPERIENCE Machine Learning Architect Hulu 2019 - current Junior Machine Learning Engineer ServiceNow 2017 - 2019 Machine Learning Intern Illumina 2016 - 2017 EDUCATION Bachelor of Science Computer Science University of California 2013 - 2017 SKILLS Pandas TensorFlow"
test_octavia = "Octavia Blackwood WORK EXPERIENCE Cofactor Genomics - Data Entry Specialist 2022 - current PROJECTS ImageRecog 2022 Be A Tech Savvy Community 2021 EDUCATION University of Michigan 2020 - current"
test_surya = "Surya Teja Menta Senior Data Scientist with 4+ years of experience Work Experience - Senior Data Scientist - Robert Bosch (Jan 2024 - preset) - Subject Matter Expert (Data Analyst) - Tudip Technologies (Oct 2020 - Oct 2023) Projects ..."

print("Atticus:")
print(calculate_total_experience(test_atticus))
print("\nOctavia:")
print(calculate_total_experience(test_octavia))
print("\nSurya:")
print(calculate_total_experience(test_surya))
