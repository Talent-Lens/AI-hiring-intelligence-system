import re
from NLP_Engine.skill_extractor import normalize_skills
from NLP_Engine.skill_db import ALL_SKILLS
from NLP_Engine.skill_db import MASTER_SKILLS
from NLP_Engine.experience_extractor import extract_required_experience
from NLP_Engine.explanation_engine import detect_domain
SOFT_SKILLS = MASTER_SKILLS["soft_skills"]

# ----------------------------
# CONFIG
# ----------------------------

MANDATORY_KEYWORDS = ["must", "required", "mandatory", "essential"]
PREFERRED_KEYWORDS = ["preferred", "nice to have", "plus", "desirable"]

DEFAULT_WEIGHT = 2
MANDATORY_WEIGHT = 3
PREFERRED_WEIGHT = 1

# Words/phrases that should NEVER be treated as skills.
# These are generic JD language that spaCy noun-chunks incorrectly surfaces.
BLACKLIST_SKILLS = {
    # Generic JD filler
    "experience", "year", "years", "knowledge", "skills", "ability", "abilities",
    "responsibilities", "responsible", "work", "job", "role", "project", "team",
    "projects", "working", "preferred", "required", "all aspects", "a culture",
    "top talent", "data-driven insights", "data driven insights", "best practices",
    "key responsibilities", "key skills", "strong background", "proven track record",
    "track record", "fast-paced", "high-growth", "growth organizations",
    "business objectives", "business goals", "business growth", "all aspects",
    "equivalent", "related field", "bachelor", "master", "degree", "education",
    "candidate", "ideal candidate", "organization", "company", "culture",
    "environment", "industry", "sector", "function", "area",
    # Adjective-heavy noise
    "strong", "excellent", "good", "solid", "extensive", "proven", "relevant",
    "progressive", "equivalent", "exceptional", "effective", "efficient",
    # Vague soft-skill noise (keep real ones in ALL_SKILLS but block generic JD phrasing)
    "negotiation skills", "communication skills", "leadership skills",
    "interpersonal skills", "analytical skills", "organizational skills",
    "management skills", "presentation skills",
}

# Phrases to strip from JD text before parsing (remove filler that confuses extraction)
STOP_PHRASES = [
    "strong experience", "experience in", "experience with",
    "knowledge of", "understanding of", "familiar with",
    "proven experience", "demonstrated experience",
    "solid understanding", "solid experience",
    "working knowledge of", "hands-on experience",
]

REMOVE_WORDS = ["preferred", "required", "must", "should", "nice to have"]


# ----------------------------
# TEXT CLEANING
# ----------------------------

def clean_job_text(text: str) -> str:
    text = text.lower()
    text = text.replace(",", " ")
    text = text.replace("(", " ")
    text = text.replace(")", " ")
    # Do NOT replace "/" — it's part of skills like "ci/cd", "ui/ux", "b2b/b2c"

    for phrase in STOP_PHRASES:
        text = text.replace(phrase, " ")
    for word in REMOVE_WORDS:
        # whole-word replace only
        text = re.sub(r"\b" + re.escape(word) + r"\b", " ", text)

    # Collapse extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ----------------------------
# SKILL EXTRACTION (DB-only, no phrase fallback)
# ----------------------------

def extract_skills(text: str) -> list:
    """
    Extracts skills by matching against ALL_SKILLS only.
    Longest-match-first prevents partial matches (e.g. 'python' inside 'python3').
    """
    text_lower = text.lower()
    extracted = set()

    # Sort longest first so multi-word skills match before their sub-words
    all_skills_sorted = sorted(ALL_SKILLS, key=len, reverse=True)

    for skill in all_skills_sorted:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            extracted.add(skill)

    # Remove anything on the blacklist
    extracted = {s for s in extracted if s not in BLACKLIST_SKILLS}

    return list(extracted)


# ----------------------------
# JD SUMMARY — CONFIG
# ----------------------------

EDUCATION_LEVELS = [
    ("PhD",        r"\b(ph\.?d\.?|doctorate)\b"),
    ("Master's",   r"\b(master'?s?(?:\s+degree)?|m\.?tech|m\.?s\.?(?!c)|mba|m\.?sc)\b"),
    ("Bachelor's", r"\b(bachelor'?s?(?:\s+degree)?|b\.?tech|b\.?e\.?|b\.?sc|undergraduate degree)\b"),
    ("Diploma",    r"\bdiploma\b"),
]

EMPLOYMENT_TYPES = [
    ("Internship", r"\bintern(?:ship)?\b"),
    ("Contract",   r"\b(contract|contractor|freelance|temporary)\b"),
    ("Part-Time",  r"\bpart[\s\-]?time\b"),
    ("Full-Time",  r"\bfull[\s\-]?time\b"),
]

WORK_MODES = [
    ("Remote",  r"\bremote\b"),
    ("Hybrid",  r"\bhybrid\b"),
    ("On-site", r"\b(on[\s\-]?site|in[\s\-]?office|in[\s\-]?person)\b"),
]

TITLE_LABEL_PATTERN = r"(?:job\s*title|position|role)\s*[:\-]\s*(.+)"

SENIORITY_LEADERSHIP = r"\b(principal|staff engineer|director|vp|vice president|head of|chief)\b"
SENIORITY_SENIOR      = r"\b(senior|sr\.?|lead)\b"
SENIORITY_ENTRY       = r"\b(junior|jr\.?|entry[\s\-]?level|associate|graduate)\b"
SENIORITY_INTERN      = r"\b(intern|internship)\b"


# ----------------------------
# JD SUMMARY — FIELD EXTRACTORS
# ----------------------------

def extract_job_title(text: str) -> str:
    """
    Attempts to identify the job title — either from an explicit
    'Job Title:' / 'Position:' / 'Role:' label, or the first short,
    title-like line of the JD (most postings open with the title).
    """
    TITLE_LABEL_PATTERN = r"\b(?:job\s*title|position|role|title)\s*[:\-]\s*(.+)"
    label_match = re.search(TITLE_LABEL_PATTERN, text, re.IGNORECASE)
    if label_match:
        title = label_match.group(1).strip()
        title = re.sub(r"^[\s#*_\-•]+", "", title)
        title = re.sub(r"[\s*_\-#]+$", "", title)
        title = title.split("\n")[0].strip()
        if title and len(title) >= 3:
            return title[:80]

    BLACKLIST_TITLE_LINES = {
        "job description", "about us", "who we are", "responsibilities", "requirements",
        "qualifications", "summary", "overview", "role summary", "job summary", "company overview",
        "description", "position details", "job details", "role overview", "welcome", "introduction"
    }

    for line in text.strip().split("\n"):
        line_clean = re.sub(r"^[\s#*_\-•]+", "", line).strip()
        line_clean = re.sub(r"[\s*_\-#]+$", "", line_clean).strip()
        if not line_clean:
            continue

        if 3 <= len(line_clean) <= 80 and not line_clean.endswith((".", ":", "?", "!")):
            if line_clean.lower() not in BLACKLIST_TITLE_LINES:
                return line_clean

    return "Not specified"


def extract_education_requirement(text: str) -> str:
    text_lower = text.lower()
    
    if re.search(r"\b(ph\.?d\.?|doctorate)\b", text_lower):
        return "PhD"
        
    if re.search(r"\b(master'?s?(?:\s+degree)?|m\.?tech|m\.?s\.?(?!c|ql)|mba|m\.?sc)\b", text_lower):
        if not re.search(r"\b(mastering|master\s+level|master\s+branch|scrum\s+master|master\s+class)\b", text_lower):
            return "Master's"
            
    if re.search(r"\b(bachelor'?s?(?:\s+degree)?|b\.?tech|b\.?e\.?|b\.?sc|undergraduate degree)\b", text_lower):
        return "Bachelor's"
        
    if re.search(r"\bdiploma\b", text_lower):
        return "Diploma"
        
    return "Not specified"


def extract_employment_type(text: str) -> str:
    text_lower = text.lower()
    
    type_label_match = re.search(r"\b(?:employment\s+type|job\s+type|type)\s*[:\-]\s*([a-zA-Z\s\-]+)", text_lower)
    if type_label_match:
        val = type_label_match.group(1).strip()
        if "full" in val:
            return "Full-Time"
        if "part" in val:
            return "Part-Time"
        if "contract" in val or "freelance" in val:
            return "Contract"
        if "intern" in val:
            return "Internship"

    is_intern = re.search(r"\bintern(?:ship)?\b", text_lower) and not re.search(r"\b(?:no|not\s+offering)\s+internships?\b", text_lower)
    is_contract = re.search(r"\b(contract|contractor|freelance|temporary)\b", text_lower) and not re.search(r"\b(?:no|no\s+third\s+party|no\s+c2c)\s+contractors?\b", text_lower)
    is_part_time = re.search(r"\bpart[\s\-]?time\b", text_lower)
    is_full_time = re.search(r"\bfull[\s\-]?time\b", text_lower)
    
    if is_intern:
        return "Internship"
    if is_contract:
        return "Contract"
    if is_part_time:
        return "Part-Time"
    if is_full_time:
        return "Full-Time"
        
    return "Not specified"


def extract_work_mode(text: str) -> str:
    text_lower = text.lower()
    
    if re.search(r"\bhybrid\b", text_lower):
        return "Hybrid"
        
    sentences = re.split(r"[.\n]", text_lower)
    has_remote = False
    remote_is_forbidden = False
    
    for sentence in sentences:
        if "remote" in sentence:
            has_remote = True
            if any(neg in sentence for neg in ["no ", "not ", "non-", "never", "unlikely", "forbidden", "prohibited", "isn't", "not available"]):
                remote_is_forbidden = True
                
    if has_remote and not remote_is_forbidden:
        return "Remote"
        
    if re.search(r"\b(on[\s\-]?site|in[\s\-]?office|in[\s\-]?person|office[\s\-]?based)\b", text_lower):
        return "On-site"
        
    if has_remote and remote_is_forbidden:
        return "On-site"
        
    return "Not specified"


def determine_seniority(required_experience_years: int, text: str, job_title: str = "") -> str:
    title_lower = job_title.lower() if job_title else ""
    if title_lower:
        if re.search(r"\b(intern|internship)\b", title_lower):
            return "Internship"
        if re.search(r"\b(principal|staff engineer|director|vp|vice president|head of|chief)\b", title_lower):
            return "Leadership / Principal"
        if re.search(r"\b(senior|sr\.?|lead)\b", title_lower):
            return "Senior"
        if re.search(r"\b(junior|jr\.?|entry[\s\-]?level|associate|graduate)\b", title_lower):
            return "Entry-Level"

    if required_experience_years >= 6:
        return "Senior"
    elif 2 <= required_experience_years < 6:
        return "Mid-Level"
    elif required_experience_years == 1:
        return "Entry-Level"

    text_lower = text.lower()
    
    if re.search(r"\b(principal|staff engineer|director|vp|vice president|head of|chief)\b", text_lower):
        if not re.search(r"report\s+to\s+(?:the\s+)?(?:principal|director|vp|head)", text_lower):
            return "Leadership / Principal"
            
    if re.search(r"\b(senior|sr\.?|lead)\b", text_lower):
        return "Senior"
        
    if re.search(r"\b(junior|jr\.?|entry[\s\-]?level|associate|graduate)\b", text_lower):
        if not re.search(r"mentor\s+(?:junior|entry|associate|graduates?)", text_lower):
            return "Entry-Level"
            
    if re.search(r"\b(intern|internship)\b", text_lower):
        return "Internship"
        
    return "Mid-Level"


def generate_jd_summary(job_text: str, required_skills, preferred_skills, skill_weights: dict) -> dict:
    """
    Builds a clear, structured, at-a-glance summary of a job description:
    title, seniority, required experience, education, employment type,
    work mode, domain, and ranked skill lists.
    """
    experience_result = extract_required_experience(job_text)
    required_years = experience_result["years"]
    experience_source = experience_result["source"]

    # Rank skills by their computed weight so the most important ones surface first
    ranked_required = sorted(required_skills, key=lambda s: skill_weights.get(s, 0), reverse=True)
    ranked_preferred = sorted(preferred_skills, key=lambda s: skill_weights.get(s, 0), reverse=True)

    domain = detect_domain(list(required_skills) + list(preferred_skills))
    job_title = extract_job_title(job_text)

    return {
        "job_title": job_title,
        "domain": domain,
        "seniority_level": determine_seniority(required_years, job_text, job_title),
        "required_experience_years": required_years if experience_source == "stated" else None,
        "required_experience_source": experience_source,
        "employment_type": extract_employment_type(job_text),
        "work_mode": extract_work_mode(job_text),
        "education_requirement": extract_education_requirement(job_text),
        "required_skills": ranked_required,
        "preferred_skills": ranked_preferred,
        "total_skills_identified": len(skill_weights),
    }


# ----------------------------
# JOB PARSER
# ----------------------------

def build_job_data(job_text: str) -> dict:
    """
    Parses a job description and returns structured skill data with weights.
    Only skills found in ALL_SKILLS (the master DB) are considered —
    no NLP noun-chunk fallback, which was the source of garbage tokens.
    """
    job_text_clean = clean_job_text(job_text)
    job_text_lower = job_text_clean.lower()
    # Split sentences from the ORIGINAL text (line breaks intact), not the
    # cleaned text — clean_job_text() collapses all whitespace including
    # newlines, so splitting on \n afterward would never actually separate
    # bullet points, causing every requirement in the JD (mandatory and
    # "nice to have" alike) to be merged into one giant sentence.
    sentences = re.split(r"[.\n]", job_text.lower())

    # Many JDs put "Required:" / "Nice to have:" as a standalone heading,
    # with the actual skills listed on separate bullet lines below that
    # don't repeat the keyword. Track the most recent heading's mode so
    # those bullets still get classified correctly instead of falling
    # through as neutral.
    HEADING_MAX_LEN = 40
    sentence_context = []
    current_mode = None
    for sentence in sentences:
        s_stripped = sentence.strip().lstrip("-•*").strip()
        if any(kw in s_stripped for kw in MANDATORY_KEYWORDS):
            current_mode = "mandatory"
        elif any(kw in s_stripped for kw in PREFERRED_KEYWORDS):
            current_mode = "preferred"
        elif s_stripped.endswith(":") and len(s_stripped) <= HEADING_MAX_LEN:
            # A short, unrelated heading (e.g. "Responsibilities:") resets context
            current_mode = None
        sentence_context.append(current_mode)

    extracted_skills = set(extract_skills(job_text_clean))

    required_skills = set()
    preferred_skills = set()
    skill_weights = {}

    for skill in extracted_skills:
        pattern = r"\b" + re.escape(skill) + r"\b"
        frequency = len(re.findall(pattern, job_text_lower))

    # Soft skills get a low fixed weight and can NEVER be mandatory —
    # they're rarely stated explicitly in resumes and shouldn't drive
    # missing-skill penalties.
        if skill in SOFT_SKILLS:
            skill_weights[skill] = 1
            continue

        if frequency >= 4:
            weight = 2.7
        elif frequency >= 2:
            weight = 2.4
        else:
            weight = DEFAULT_WEIGHT

        for idx, sentence in enumerate(sentences):
            if re.search(pattern, sentence):
                if any(kw in sentence for kw in MANDATORY_KEYWORDS):
                    required_skills.add(skill)
                    weight = MANDATORY_WEIGHT
                    break
                elif any(kw in sentence for kw in PREFERRED_KEYWORDS):
                    preferred_skills.add(skill)
                    weight = max(weight, PREFERRED_WEIGHT)
                elif sentence_context[idx] == "mandatory":
                    required_skills.add(skill)
                    weight = MANDATORY_WEIGHT
                    break
                elif sentence_context[idx] == "preferred":
                    preferred_skills.add(skill)
                    weight = max(weight, PREFERRED_WEIGHT)

        skill_weights[skill] = weight

    summary = generate_jd_summary(job_text, required_skills, preferred_skills, skill_weights)

    return {
        "text": job_text,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "skill_weights": skill_weights,
        "summary": summary,
    }