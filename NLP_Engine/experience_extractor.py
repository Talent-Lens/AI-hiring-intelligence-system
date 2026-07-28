import re
from datetime import datetime


# =============================================================================
# TOTAL EXPERIENCE EXTRACTION
# =============================================================================

def calculate_total_experience(text: str) -> dict:
    """
    Extracts total years of professional experience from resume text.

    Returns a dict:
        {"years": float, "source": "calculated" | "claimed" | "unknown"}

    Source meanings:
        "calculated" — real date ranges found and summed (most reliable)
        "claimed"    — only an explicit "X years experience" statement found
        "unknown"    — nothing found; returns 0.5 as a safe fallback
    """

    current_date  = datetime.now()
    current_year  = current_date.year
    current_month = current_date.month

    # ── Normalise dash variants ───────────────────────────────────────────────
    text = (text
            .replace("\u2013", "-")   # en-dash
            .replace("\u2014", "-")   # em-dash
            .replace("\u2212", "-"))  # minus sign

    # =========================================================================
    # 1. SECTION IDENTIFICATION — skip EDUCATION to avoid degree years
    # =========================================================================
    section_headers = [
        ("EXP",      r"\b(WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY|WORK HISTORY|EXPERIENCE)\b"),
        ("EDU",      r"\b(EDUCATION|ACADEMIC BACKGROUND|SCHOLASTIC|ACADEMIC QUALIFICATIONS)\b"),
        ("PROJECTS", r"\b(PROJECTS|PERSONAL PROJECTS|ACADEMIC PROJECTS)\b"),
        ("SKILLS",   r"\b(SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES)\b"),
        ("SUMMARY",  r"\b(SUMMARY|OBJECTIVE|PROFILE|ABOUT ME|CAREER OBJECTIVE)\b"),
        ("CERTS",    r"\b(CERTIFICATIONS?|CERTIFICATES?|TRAINING|COURSES?|LICENSES?)\b"),
    ]

    found_headers = []
    for tag, pattern in section_headers:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            found_headers.append((m.start(), tag))
    found_headers.sort()

    segments = []
    if not found_headers:
        segments.append(("UNKNOWN", text))
    else:
        if found_headers[0][0] > 0:
            segments.append(("HEADERLESS", text[:found_headers[0][0]]))
        for i, (start_idx, tag) in enumerate(found_headers):
            end_idx = found_headers[i + 1][0] if i + 1 < len(found_headers) else len(text)
            segments.append((tag, text[start_idx:end_idx]))

    # =========================================================================
    # 2. DATE RANGE PATTERNS
    # =========================================================================

    # Building blocks
    PRESENT_WORDS = (
        r"(?:present|current|now|today"
        r"|till\s+date|to\s+date"
        r"|till\s+now|ongoing|continue[sd]?)"
    )

    month_word = (
        r"(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?"
        r"|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?"
        r"|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
    )
    month_num  = r"(?:0?[1-9]|1[0-2])"
    year_4     = r"(?:19|20)\d{2}"       # strict — avoids matching random numbers

    opt_month  = rf"(?:(?:{month_word}|{month_num})[/\-\.\s]{{0,3}})?"

    # Separator: –, —, -, "to" (only when not "to date"), "till" (only when not "till date")
    separator = r"(?:–|—|-|\bto(?!\s+date)\b|\btill(?!\s+date)\b)"

    # Pattern A — explicit separator between two dates/present
    # Captures: (start_year, end_year, present_flag)
    main_pattern = (
        rf"{opt_month}({year_4})"
        rf"\s*{separator}\s*"
        rf"(?:{opt_month}({year_4})|({PRESENT_WORDS}))"
    )

    # Pattern B — "YEAR till/to date" with no dash separator (common in Indian CVs)
    # e.g. "Apr 2018 till date", "2018 to date"
    present_only_pattern = (
        rf"{opt_month}({year_4})\s+({PRESENT_WORDS})"
    )

    # Pattern C — apostrophe-prefixed 2-digit years: '12 to '16
    apos_pattern = (
        rf"'(\d{{2}})\s*(?:–|—|-|\bto\b|\btill\b)\s*"
        rf"(?:'(\d{{2}})|({PRESENT_WORDS}))"
    )

    # =========================================================================
    # 3. EXTRACT DATE RANGES
    # =========================================================================
    ranges = []

    def add_range(start_y: int, end_y: int, end_m: int = None):
        """Sanity-check and append a date range."""
        if end_m is None:
            end_m = current_month if end_y == current_year else 12
        if not (1950 <= start_y <= current_year):
            return
        if not (1950 <= end_y <= current_year):
            return
        start_val = start_y * 12 + 1       # assume January start if no month given
        end_val   = end_y * 12 + end_m
        if start_val < end_val:
            ranges.append((start_val, end_val))

    for tag, seg_text in segments:
        # Always skip education section — degree years cause false positives
        if tag in ("EDU", "CERTS"):
            continue

        # Pattern A — main range with separator
        for m in re.finditer(main_pattern, seg_text, re.IGNORECASE):
            try:
                start_y = int(m.group(1))
                end_y   = current_year if m.group(3) else int(m.group(2))
                end_m   = current_month if m.group(3) else None
                add_range(start_y, end_y, end_m)
            except Exception:
                continue

        # Pattern B — "YEAR till/to date" (no dash)
        for m in re.finditer(present_only_pattern, seg_text, re.IGNORECASE):
            try:
                start_y = int(m.group(1))
                add_range(start_y, current_year, current_month)
            except Exception:
                continue

        # Pattern C — apostrophe years '12 to '16
        for m in re.finditer(apos_pattern, seg_text, re.IGNORECASE):
            try:
                start_y = 2000 + int(m.group(1))
                end_y   = current_year if m.group(3) else 2000 + int(m.group(2))
                end_m   = current_month if m.group(3) else None
                add_range(start_y, end_y, end_m)
            except Exception:
                continue

    # =========================================================================
    # 4. EXPLICIT "X YEARS EXPERIENCE" FALLBACK
    # =========================================================================
    explicit_val = 0.0
    explicit_match = re.search(
        r"(\d+(?:\.\d+)?)\+?\s*years?\s*(?:of\s*)?(?:relevant\s*|professional\s*)?experience",
        text,
        re.IGNORECASE,
    )
    if explicit_match:
        try:
            explicit_val = float(explicit_match.group(1))
        except Exception:
            pass

    # =========================================================================
    # 5. IF NO DATE RANGES FOUND — use explicit claim or unknown fallback
    # =========================================================================
    if not ranges:
        if explicit_val > 0:
            return {"years": round(explicit_val, 1), "source": "claimed"}
        return {"years": 0.5, "source": "unknown"}

    # =========================================================================
    # 6. MERGE OVERLAPPING RANGES & SUM
    # =========================================================================
    ranges.sort()
    total_months = 0
    curr_s, curr_e = ranges[0]
    for next_s, next_e in ranges[1:]:
        if next_s <= curr_e:                    # overlapping — extend current
            curr_e = max(curr_e, next_e)
        else:                                   # gap — commit current, start new
            total_months += (curr_e - curr_s)
            curr_s, curr_e = next_s, next_e
    total_months += (curr_e - curr_s)

    calculated_val = round(total_months / 12.0, 1)

    if calculated_val > 0:
        return {"years": calculated_val, "source": "calculated"}

    if explicit_val > 0:
        return {"years": round(explicit_val, 1), "source": "claimed"}

    return {"years": 0.5, "source": "unknown"}


# =============================================================================
# SECTION EXTRACTION (used by resume_parser.py)
# =============================================================================

def split_resume_into_sections(text: str) -> dict:
    """
    Splits resume text into logical sections based on common section headers.
    Returns a dict mapping section tag → text content.
    """
    headers = [
        ("EXPERIENCE",     r"\b(WORK EXPERIENCE|EXPERIENCE|PROFESSIONAL EXPERIENCE|EMPLOYMENT HISTORY|WORK HISTORY|CAREER HISTORY)\b"),
        ("PROJECTS",       r"\b(PROJECTS|PERSONAL PROJECTS|ACADEMIC PROJECTS|RELEVANT PROJECTS|KEY PROJECTS)\b"),
        ("INTERNSHIP",     r"\b(INTERNSHIP|INTERNSHIPS|TRAINEE|VOLUNTEER|VOLUNTEERING)\b"),
        ("RESEARCH",       r"\b(RESEARCH|PUBLICATIONS|ACHIEVEMENTS|AWARDS|HONORS|HONOURS|ACCOMPLISHMENTS)\b"),
        ("SKILLS",         r"\b(SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES|KEY COMPETENCIES|PROFICIENCIES|AREAS OF EXPERTISE)\b"),
        ("CERTIFICATIONS", r"\b(CERTIFICATIONS?|CERTIFICATES?|COURSES?|EDUCATION|TRAINING|LICENSES?|QUALIFICATIONS?)\b"),
        ("SUMMARY",        r"\b(SUMMARY|OBJECTIVE|PROFILE|ABOUT ME|CAREER OBJECTIVE|PROFESSIONAL SUMMARY|PERSONAL STATEMENT)\b"),
        ("KEYWORDS",       r"\b(KEYWORDS|TOOLS|TECHNOLOGIES|TECH STACK)\b"),
    ]

    found_headers = []
    for tag, pattern in headers:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            found_headers.append((m.start(), tag))
    found_headers.sort()

    sections = {}

    if not found_headers:
        sections["UNKNOWN"] = text
        return sections

    if found_headers[0][0] > 0:
        sections["HEADER"] = text[:found_headers[0][0]]

    for i, (start_idx, tag) in enumerate(found_headers):
        end_idx = found_headers[i + 1][0] if i + 1 < len(found_headers) else len(text)
        content = text[start_idx:end_idx].strip()
        if tag in sections:
            sections[tag] += "\n" + content
        else:
            sections[tag] = content

    return sections


# =============================================================================
# REQUIRED EXPERIENCE (used by job_parser.py and matcher.py)
# =============================================================================

def extract_required_experience(job_text: str) -> dict:
    """
    Pulls the minimum years of experience required from a job description.

    Returns a dict:
        {"years": int, "source": "stated" | "default"}

    "stated" — the JD explicitly mentions a years-of-experience requirement.
    "default" — nothing was found; falls back to 3 (safe mid-level assumption)
    """
    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
    }
    
    # Regex matching digit or word number, and allowing descriptive terms like "software engineering" between years and experience
    match = re.search(
        r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\+?\s*(?:to\s*\d+)?\s*years?\s*(?:of\s*)?(?:\s*[a-zA-Z\s\-]{0,25})?\s*experience",
        job_text,
        re.IGNORECASE
    )
    if match:
        val = match.group(1).lower()
        years = int(val) if val.isdigit() else word_to_num.get(val, 3)
        return {"years": years, "source": "stated"}
        
    return {"years": 3, "source": "default"}