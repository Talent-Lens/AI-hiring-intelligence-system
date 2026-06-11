import spacy
import re
from spacy.matcher import PhraseMatcher
from NLP_Engine.experience_extractor import split_resume_into_sections

# Load model once
nlp = spacy.load("en_core_web_sm")

from NLP_Engine.skill_synonyms import SKILL_SYNONYMS

# Canonical skill dictionary (normalized form) - Expanded from synonyms
SKILL_DB = {}
for canonical, synonyms in SKILL_SYNONYMS.items():
    SKILL_DB[canonical] = [canonical] + synonyms

# Add some extras not in synonyms
EXTRA_SKILLS = {
    "git": ["git", "github", "gitlab"],
    "docker": ["docker"],
    "kubernetes": ["k8s", "kubernetes"],
    "aws": ["aws", "amazon web services"],
    "sql": ["sql", "mysql", "postgresql", "oracle", "mariadb"],
    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node", "nodejs", "node.js"]
}
for k, v in EXTRA_SKILLS.items():
    if k in SKILL_DB:
        SKILL_DB[k] = list(set(SKILL_DB[k] + v))
    else:
        SKILL_DB[k] = v

def normalize_skills(skills):
    from NLP_Engine.skill_synonyms import normalize_skills as ns
    return ns(skills)

def normalize_skills(skills):

    normalized = set()

    for skill in skills:
        skill = skill.lower().strip()

        mapped = False

        for canonical, synonyms in SKILL_SYNONYMS.items():
            if skill == canonical or skill in synonyms:
                normalized.add(canonical)
                mapped = True
                break

        if not mapped:
            normalized.add(skill)

    return normalized
# Build matcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

for canonical, variations in SKILL_DB.items():
    patterns = [nlp.make_doc(text) for text in variations]
    matcher.add(canonical, patterns)


def score_evidence_quality(text, skill_name):
    text_lower = text.lower()
    score = 0
    
    # Action verbs indicate real experience vs just a list
    action_verbs = ["developed", "built", "implemented", "managed", "using", "created", "designed", "optimized", "architected"]
    if any(verb in text_lower for verb in action_verbs):
        score += 10
        
    # Penalize giant lists (common in "Skills" sections)
    comma_count = text.count(',')
    if comma_count > 8:
        score -= 15
    if len(text) > 300:
        score -= 10
        
    # Preference for "Experience" context
    if "experience" in text_lower or "worked with" in text_lower:
        score += 5
        
    return score

def extract_skills(text: str, include_evidence: bool = False):
    doc = nlp(text)
    matches = matcher(doc)

    if not include_evidence:
        extracted = set()
        for match_id, start, end in matches:
            skill_name = nlp.vocab.strings[match_id]
            extracted.add(skill_name)
        return list(extracted)
    
    skill_evidence = {}
    evidence_scores = {}
    
    # Pre-split text into lines to handle bullet points better
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    for match_id, start, end in matches:
        skill_name = nlp.vocab.strings[match_id]
        span = doc[start:end]
        
        matched_text = span.text
        raw_evidence = span.sent.text.strip()
        
        # Heuristic: If the sentence is huge (likely a block), try to find a tighter line
        best_line = raw_evidence
        for line in lines:
            if matched_text in line:
                if len(line) < len(best_line):
                    best_line = line
                elif len(line) < 150: # Prefer lines over huge sentences
                    best_line = line
                    break
        
        evidence = " ".join(best_line.split())
        
        # NEW: If the resulting evidence is still very long, it's likely a dense list.
        # Try to split by common list separators (comma, semicolon, bullet)
        # NEW: Aggressive isolation for dense skill blocks
        # NEW: Aggressive sub-item isolation for dense skill blocks
        if len(evidence) > 60:
            match_start = evidence.lower().find(matched_text.lower())
            if match_start != -1:
                # Find context boundaries (commas, newlines, colons)
                # We want to keep the "Category:" if it's right before the skill
                # Split by delimiters but Keep the delimiters to avoid losing info if needed
                # Actually, simpler: find the part containing the skill
                # Standardize separators
                temp_evidence = evidence.replace(';', ',').replace('•', ',')
                parts = temp_evidence.split(',')
                
                found_iso = False
                for part in parts:
                    if matched_text.lower() in part.lower():
                        iso_part = part.strip()
                        
                        # Case 1: The part itself contains the header (e.g. "Tools: Git")
                        if ":" in iso_part:
                             bits = iso_part.split(":")
                             header_part = bits[0].strip() + ": "
                             if matched_text.lower() in bits[-1].lower():
                                 evidence = header_part + bits[-1].strip()
                                 found_iso = True
                             else:
                                 evidence = iso_part
                                 found_iso = True
                        
                        # Case 2: The header is further back in the line
                        else:
                             start_idx = evidence.lower().find(iso_part.lower())
                             pre_text = evidence[:start_idx]
                             if ":" in pre_text:
                                  # Find the nearest colon and the word right before it
                                  # We split by colon and take the last bit
                                  header_candidate = pre_text.split(":")[-1].strip()
                                  
                                  # If the text between the colon and our skill is long, 
                                  # it's likely other skills, NOT a header.
                                  if len(header_candidate) > 20: 
                                       # Look for the word before the colon itself
                                       main_header = pre_text.split(":")[-2].strip().split()[-1]
                                       evidence = main_header + ": " + iso_part
                                  else:
                                       evidence = header_candidate + ": " + iso_part
                             else:
                                  evidence = iso_part
                             found_iso = True
                        break
                
                # If we couldn't isolate via commas, at least try a firm truncation
                if not found_iso and len(evidence) > 100:
                    evidence = evidence[:97] + "..."






        evidence = re.sub(r'^[•\-\*\s]+', '', evidence)
        
        # Limit length firmly
        if len(evidence) > 250:
            evidence = evidence[:247] + "..."
            
        current_score = score_evidence_quality(evidence, skill_name)
        
        if skill_name not in skill_evidence or current_score > evidence_scores.get(skill_name, -99):
            skill_evidence[skill_name] = evidence
            evidence_scores[skill_name] = current_score

    return skill_evidence

def classify_skills_by_section(text: str, required_skills: set = None, semantic_matches: dict = None):
    """
    Classifies skills into Demonstrated vs Mentioned Only based on resume sections.
    Handles semantic matches if provided (mapping required_skill -> resume_skill).
    """
    sections = split_resume_into_sections(text)
    
    DEMONSTRATED_TAGS = ["EXPERIENCE", "PROJECTS", "INTERNSHIP", "RESEARCH"]
    MENTIONED_TAGS = ["SKILLS", "CERTIFICATIONS", "KEYWORDS", "HEADER", "UNKNOWN"]
    
    categorized_skills = {
        "Demonstrated": {}, # skill: evidence
        "Mentioned Only": {}, # skill: "Mentioned in Skills section..."
        "Not Found": []
    }
    
    # 1. Extract skills from Demonstrated sections
    demo_sections_present = [tag for tag in DEMONSTRATED_TAGS if tag in sections]
    
    # If no demonstrated sections found, but we have UNKNOWN, treat UNKNOWN as demonstrated
    if not demo_sections_present and "UNKNOWN" in sections:
        all_demo_text = sections["UNKNOWN"]
    else:
        all_demo_text = "\n".join([sections[tag] for tag in demo_sections_present])
        
    demo_evidence = extract_skills(all_demo_text, include_evidence=True)
    
    # 2. Extract skills from Mentioned sections
    mentioned_sections_present = [tag for tag in MENTIONED_TAGS if tag in sections and (tag != "UNKNOWN" or not all_demo_text == sections["UNKNOWN"])]
    all_mentioned_text = "\n".join([sections[tag] for tag in mentioned_sections_present])
    mentioned_evidence = extract_skills(all_mentioned_text, include_evidence=True)
    
    # 3. Combine for easy lookup
    all_found_evidence = {**mentioned_evidence, **demo_evidence}
    
    # 4. Classify targets
    target_skills = required_skills if required_skills else set(all_found_evidence.keys())
    semantic_matches = semantic_matches or {}
    
    for skill in target_skills:
        skill_lower = skill.lower()
        
        # Scenario A: Exact (or direct synonym) match in Demonstrated
        found_in_demo = False
        for s_name, evidence in demo_evidence.items():
            if s_name.lower() == skill_lower:
                categorized_skills["Demonstrated"][s_name] = evidence
                found_in_demo = True
                break
        if found_in_demo: continue
            
        # Scenario B: Semantic match to a Demonstrated skill
        # (e.g. required "scikit-learn" matches resume "machine learning")
        if skill_lower in semantic_matches:
            res_skill = semantic_matches[skill_lower]
            # Check if this resume skill was found in a Demonstrated section
            found_res_in_demo = False
            for s_name, evidence in demo_evidence.items():
                if s_name.lower() == res_skill.lower():
                    categorized_skills["Demonstrated"][skill] = f"(Semantic Match via '{res_skill}') {evidence}"
                    found_res_in_demo = True
                    break
            if found_res_in_demo: continue

        # Scenario C: Exact (or direct synonym) match in Mentioned Only
        found_in_mentioned = False
        for s_name, _ in mentioned_evidence.items():
            if s_name.lower() == skill_lower:
                categorized_skills["Mentioned Only"][s_name] = "Listed in Skills or Certifications section but no project or experience evidence found."
                found_in_mentioned = True
                break
        if found_in_mentioned: continue
            
        # Scenario D: Semantic match to a Mentioned Only skill
        if skill_lower in semantic_matches:
            res_skill = semantic_matches[skill_lower]
            found_res_in_mentioned = False
            for s_name in mentioned_evidence.keys():
                if s_name.lower() == res_skill.lower():
                    categorized_skills["Mentioned Only"][skill] = f"Semantically matched to '{res_skill}' in Skills section, but no experience evidence found."
                    found_res_in_mentioned = True
                    break
            if found_res_in_mentioned: continue
            
        # Scenario E: Not Found
        categorized_skills["Not Found"].append(skill)
            
    return categorized_skills
