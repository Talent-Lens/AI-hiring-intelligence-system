import re
from datetime import datetime


def calculate_total_experience(text: str) -> float:
    current_date = datetime.now()

    # -----------------------------------------------
    # CLEAN
    # -----------------------------------------------
    text = re.sub(r'[\xa0\u00a0\u202f\u2009\u200b\u2002\u2003]', ' ', text)
    text = re.sub(r'[–—−‐]', '-', text)
    text = text.replace('\uf0b7', ' ').replace('●', ' ')

    # Collapse spaced letters including mixed 1-2 char tokens
    # Handles: "J A N U A R Y", "N OV E M B E R", "F E B R U A RY", "T R AV E L"
    text = re.sub(
        r'(?<![A-Za-z])(?:[A-Za-z]{1,2} ){2,}[A-Za-z]+(?![A-Za-z])',
        lambda m: m.group(0).replace(' ', ''),
        text
    )

    # Collapse spaced digits: "2 0 2 0" → "2020"
    text = re.sub(
        r'(?<!\d)(?:\d ){3}\d(?!\d)',
        lambda m: m.group(0).replace(' ', ''),
        text
    )

    # Fix any remaining broken month tokens e.g. "JANUA RY" → "JANUARY"
    all_months = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ]
    for month in all_months:
        for split in range(2, len(month) - 1):
            broken = month[:split] + ' ' + month[split:]
            text = text.replace(broken.upper(), month.upper())
            text = text.replace(broken.title(), month.title())
            text = text.replace(broken, month)

    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    search_text = text.lower()

    # -----------------------------------------------
    # SECTION DETECTION
    # -----------------------------------------------
    WORK_HEADERS = {
        'employment history', 'work experience', 'professional experience',
        'experience', 'work history', 'career history', 'employment',
        'positions held', 'job history', 'professional background',
        # collapsed variants
        'employmenthistory', 'workexperience', 'professionalexperience',
        'workhistory', 'careerhistory', 'professionalbackground',
        'positionsheld', 'jobhistory',
    }
    NON_WORK_HEADERS = {
        'education', 'academic background', 'qualifications',
        'courses', 'certifications', 'certification', 'training',
        'licenses', 'accomplishments', 'achievements', 'awards',
        'projects', 'volunteer experience', 'volunteering', 'references',
        'languages', 'skills', 'hobbies', 'interests', 'profile',
        'summary', 'objective', 'contact', 'details', 'links',
        'publications', 'activities', 'additional information',
        'professional development', 'extracurricular',
        # collapsed variants
        'academicbackground', 'volunteerexperience', 'additionalinformation',
        'professionaldevelopment',
    }

    section_map = [(0, False)]
    pos = 0
    for line in search_text.split('\n'):
        stripped = line.strip()
        alpha_only = re.sub(r'[^a-z\s]', '', stripped).strip()
        alpha_only = re.sub(r'\s+', ' ', alpha_only)
        alpha_collapsed = alpha_only.replace(' ', '')

        if alpha_only in WORK_HEADERS or alpha_collapsed in WORK_HEADERS:
            section_map.append((pos, True))
        elif alpha_only in NON_WORK_HEADERS or alpha_collapsed in NON_WORK_HEADERS:
            section_map.append((pos, False))

        pos += len(line) + 1

    section_map.sort()

    def is_work_section(idx: int) -> bool:
        result = False
        for p, is_work in section_map:
            if p <= idx:
                result = is_work
            else:
                break
        return result

    # -----------------------------------------------
    # DATE PARSING
    # -----------------------------------------------
    month_pat = (
        r'(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|'
        r'jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|'
        r'nov(?:ember)?|dec(?:ember)?)'
    )
    month_map = {
        'jan': 1, 'january': 1, 'feb': 2, 'february': 2,
        'mar': 3, 'march': 3, 'apr': 4, 'april': 4,
        'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
        'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
        'oct': 10, 'october': 10, 'nov': 11, 'november': 11,
        'dec': 12, 'december': 12,
    }

    date_patterns = [
        rf'(?:({month_pat})\s+)?(\d{{4}})\s*[-–/to]+\s*(?:({month_pat})\s+)?(present|\d{{4}})',
        r'(\d{1,2})/(\d{4})\s*[-–]+\s*(\d{1,2})/(present|\d{4})',
        r'\((\d{4})\s*[-–]\s*(present|\d{4})\)',
    ]

    all_periods = []

    for pattern in date_patterns:
        for m in re.finditer(pattern, search_text, re.IGNORECASE):
            try:
                g = m.groups()
                if len(g) == 2:
                    sy, ey = g
                    sm = 1
                    start_year = int(sy)
                    if str(ey).lower() == 'present':
                        end_year, em = current_date.year, current_date.month
                    else:
                        end_year, em = int(ey), 12
                elif g[0] and str(g[0]).isdigit():
                    sm_s, sy, em_s, ey = g
                    sm, start_year = int(sm_s), int(sy)
                    if ey.lower() == 'present':
                        end_year, em = current_date.year, current_date.month
                    else:
                        end_year, em = int(ey), int(em_s)
                else:
                    smon, sy, emon, ey = g
                    start_year = int(sy)
                    sm = month_map.get((smon or '').lower(), 1)
                    if ey.lower() == 'present':
                        end_year, em = current_date.year, current_date.month
                    else:
                        end_year = int(ey)
                        em = month_map.get((emon or '').lower(), 12)

                if not (1950 <= start_year <= current_date.year):
                    continue
                if not (1950 <= end_year <= current_date.year + 1):
                    continue

                start_date = datetime(start_year, sm, 1)
                end_date = datetime(end_year, em, 1)

                if end_date > start_date:
                    all_periods.append((start_date, end_date, m.start()))
            except:
                continue

    # -----------------------------------------------
    # FILTER: work section only
    # -----------------------------------------------
    work_periods = [
        (s, e) for s, e, idx in all_periods
        if is_work_section(idx)
    ]

    # -----------------------------------------------
    # FALLBACK: no section headers detected
    # -----------------------------------------------
    if not work_periods:
        edu_keywords = {
            'university', 'college', 'bachelor', 'master', 'degree',
            'diploma', 'mba', 'phd', 'certificate', 'certified',
            'school of', 'institute of',
        }
        for s, e, idx in all_periods:
            ctx = search_text[max(0, idx - 250): idx + 100]
            if not any(kw in ctx for kw in edu_keywords):
                work_periods.append((s, e))

    if not work_periods:
        return 0.1

    # -----------------------------------------------
    # MERGE OVERLAPS
    # -----------------------------------------------
    work_periods.sort()
    merged = [work_periods[0]]
    for cur in work_periods[1:]:
        last = merged[-1]
        if cur[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], cur[1]))
        else:
            merged.append(cur)

    # -----------------------------------------------
    # CALCULATE
    # -----------------------------------------------
    total_months = sum(
        (p[1].year - p[0].year) * 12 + (p[1].month - p[0].month)
        for p in merged
    )
    total_years = round(total_months / 12, 1)
    return min(max(total_years, 0.1), 40.0)