import spacy
import re
from spacy.matcher import PhraseMatcher
from NLP_Engine.experience_extractor import split_resume_into_sections
from NLP_Engine.skill_db import MASTER_SKILLS, ALL_SKILLS
from NLP_Engine.skill_synonyms import CANONICAL_MAP, normalize_skills

SOFT_SKILLS = MASTER_SKILLS["soft_skills"]

# Load spacy model once
nlp = spacy.load("en_core_web_sm")

# ── Build SKILL_DB from ALL_SKILLS + CANONICAL_MAP ───────────────────────────
# SKILL_DB maps canonical_skill -> [all surface forms that should match it]
# We build it by inverting CANONICAL_MAP: group all variants by their canonical.

SKILL_DB = {}

# Start with every skill in ALL_SKILLS as its own entry
for skill in ALL_SKILLS:
    canonical = CANONICAL_MAP.get(skill, skill)  # map to canonical if exists
    if canonical not in SKILL_DB:
        SKILL_DB[canonical] = set()
    SKILL_DB[canonical].add(skill)
    SKILL_DB[canonical].add(canonical)

# Add all variants from CANONICAL_MAP
for variant, canonical in CANONICAL_MAP.items():
    if canonical not in SKILL_DB:
        SKILL_DB[canonical] = set()
    SKILL_DB[canonical].add(variant)
    SKILL_DB[canonical].add(canonical)

# Convert sets to lists
SKILL_DB = {k: list(v) for k, v in SKILL_DB.items()}

# Add hardcoded extras that might not be in ALL_SKILLS
EXTRA_SKILLS = {
    "git":       ["git", "github", "gitlab", "bitbucket"],
    "docker":    ["docker", "docker compose"],
    "kubernetes":["k8s", "kubernetes"],
    "aws":       ["aws", "amazon web services"],
    "sql":       ["sql", "mysql", "postgresql", "oracle", "mariadb"],
    "react":     ["react", "react.js", "reactjs"],
    "node.js":   ["node", "nodejs", "node.js"],
}
for k, v in EXTRA_SKILLS.items():
    if k in SKILL_DB:
        SKILL_DB[k] = list(set(SKILL_DB[k] + v))
    else:
        SKILL_DB[k] = v

# ── Build spacy PhraseMatcher ─────────────────────────────────────────────────
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
for canonical, variations in SKILL_DB.items():
    patterns = [nlp.make_doc(text) for text in variations if text.strip()]
    if patterns:
        matcher.add(canonical, patterns)


def score_evidence_quality(text, skill_name):
    text_lower = text.lower()
    score = 0
    action_verbs = [
    # Engineering
    "developed", "built", "implemented", "architected", "optimized", "deployed",
    # Management/Leadership
    "managed", "led", "coordinated", "mentored", "supervised", "directed",
    # Business/Marketing
    "launched", "grew", "increased", "negotiated", "presented", "delivered",
    "generated", "achieved", "exceeded",
    # Research/Analysis
    "analysed", "analyzed", "researched", "evaluated", "designed", "created",
    # General positive signal
    "using", "responsible for", "spearheaded", "established"
]
    if any(verb in text_lower for verb in action_verbs):
        score += 10
    comma_count = text.count(',')
    if comma_count > 8:
        score -= 15
    if len(text) > 300:
        score -= 10
    if "experience" in text_lower or "worked with" in text_lower:
        score += 5
    return score

def _extract_skills_from_doc(doc, include_evidence: bool = False):
    """
    Core logic to extract skills from a pre-processed Spacy Doc.
    """
    matches = matcher(doc)

    if not include_evidence:
        extracted = set()
        for match_id, start, end in matches:
            skill_name = nlp.vocab.strings[match_id]
            extracted.add(skill_name)
        return list(extracted)
    
    skill_evidence = {}
    evidence_scores = {}
    
    text = doc.text
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for match_id, start, end in matches:
        skill_name = nlp.vocab.strings[match_id]
        span = doc[start:end]
        matched_text = span.text
        raw_evidence = span.sent.text.strip()
        
        best_line = raw_evidence
        for line in lines:
            if matched_text in line:
                if len(line) < len(best_line):
                    best_line = line
                elif len(line) < 150:
                    best_line = line
                    break
        
        evidence = " ".join(best_line.split())
        
        if len(evidence) > 60:
            temp_evidence = evidence.replace(';', ',').replace('•', ',')
            parts = temp_evidence.split(',')
            found_iso = False
            for part in parts:
                if matched_text.lower() in part.lower():
                    iso_part = part.strip()
                    if ":" in iso_part:
                         bits = iso_part.split(":")
                         header_part = bits[0].strip() + ": "
                         if matched_text.lower() in bits[-1].lower():
                             evidence = header_part + bits[-1].strip()
                             found_iso = True
                         else:
                             evidence = iso_part
                             found_iso = True
                    else:
                         start_idx = evidence.lower().find(iso_part.lower())
                         pre_text = evidence[:start_idx]
                         if ":" in pre_text:
                              header_candidate = pre_text.split(":")[-1].strip()
                              if len(header_candidate) > 20: 
                                   main_header = pre_text.split(":")[-2].strip().split()[-1]
                                   evidence = main_header + ": " + iso_part
                              else:
                                   evidence = header_candidate + ": " + iso_part
                         else:
                              evidence = iso_part
                         found_iso = True
                    break
            if not found_iso and len(evidence) > 100:
                evidence = evidence[:97] + "..."

        evidence = re.sub(r'^[•\-\*\s]+', '', evidence)
        if len(evidence) > 250:
            evidence = evidence[:247] + "..."
            
        current_score = score_evidence_quality(evidence, skill_name)
        if skill_name not in skill_evidence or current_score > evidence_scores.get(skill_name, -99):
            skill_evidence[skill_name] = evidence
            evidence_scores[skill_name] = current_score

    return skill_evidence

def extract_skills(text: str, include_evidence: bool = False):
    doc = nlp(text)
    return _extract_skills_from_doc(doc, include_evidence)

def batch_extract_skills(texts: list, include_evidence: bool = False):
    """
    HIGH SPEED: Extracts skills for multiple texts at once using nlp.pipe.
    """
    docs = nlp.pipe(texts)
    return [_extract_skills_from_doc(doc, include_evidence) for doc in docs]

def classify_skills_by_section(text: str, required_skills: set = None, semantic_matches: dict = None):
    sections = split_resume_into_sections(text)
    DEMONSTRATED_TAGS = ["EXPERIENCE", "PROJECTS", "INTERNSHIP", "RESEARCH"]
    MENTIONED_TAGS = ["SKILLS", "CERTIFICATIONS", "KEYWORDS", "HEADER", "UNKNOWN"]
    
    categorized_skills = {
        "Demonstrated": {}, 
        "Mentioned Only": {}, 
        "Not Found": []
    }
    
    demo_sections_present = [tag for tag in DEMONSTRATED_TAGS if tag in sections]
    if not demo_sections_present and "UNKNOWN" in sections:
        all_demo_text = sections["UNKNOWN"]
    else:
        all_demo_text = "\n".join([sections[tag] for tag in demo_sections_present])
        
    demo_evidence = extract_skills(all_demo_text, include_evidence=True)
    
    mentioned_sections_present = [tag for tag in MENTIONED_TAGS if tag in sections and (tag != "UNKNOWN" or not all_demo_text == sections["UNKNOWN"])]
    all_mentioned_text = "\n".join([sections[tag] for tag in mentioned_sections_present])
    mentioned_evidence = extract_skills(all_mentioned_text, include_evidence=True)
    
    all_found_evidence = {**mentioned_evidence, **demo_evidence}
    target_skills = required_skills if required_skills else set(all_found_evidence.keys())
    semantic_matches = semantic_matches or {}
    
    for skill in target_skills:
        skill_lower = skill.lower()
        found_in_demo = False
        for s_name, evidence in demo_evidence.items():
            if s_name.lower() == skill_lower:
                categorized_skills["Demonstrated"][s_name] = evidence
                found_in_demo = True
                break
        if found_in_demo: continue
            
        if skill_lower in semantic_matches:
            res_skill = semantic_matches[skill_lower]
            found_res_in_demo = False
            for s_name, evidence in demo_evidence.items():
                if s_name.lower() == res_skill.lower():
                    categorized_skills["Demonstrated"][skill] = f"(Semantic Match via '{res_skill}') {evidence}"
                    found_res_in_demo = True
                    break
            if found_res_in_demo: continue

        found_in_mentioned = False
        for s_name, _ in mentioned_evidence.items():
            if s_name.lower() == skill_lower:
                categorized_skills["Mentioned Only"][s_name] = "Listed in Skills or Certifications section but no project or experience evidence found."
                found_in_mentioned = True
                break
        if found_in_mentioned: continue
            
        if skill_lower in semantic_matches:
            res_skill = semantic_matches[skill_lower]
            found_res_in_mentioned = False
            for s_name in mentioned_evidence.keys():
                if s_name.lower() == res_skill.lower():
                    categorized_skills["Mentioned Only"][skill] = f"Semantically matched to '{res_skill}' in Skills section, but no experience evidence found."
                    found_res_in_mentioned = True
                    break
            if found_res_in_mentioned: continue
            
        categorized_skills["Not Found"].append(skill)
     # Hide soft skills from the "Not Found" list shown to the user
    categorized_skills["Not Found"] = [
        skill
        for skill in categorized_skills["Not Found"]
        if skill not in SOFT_SKILLS
    ]

    return categorized_skills    
    