
from NLP_Engine.advanced_skill_extractor import extract_additional_skills
from NLP_Engine.skill_extractor import extract_skills, normalize_skills
from NLP_Engine.utils import extract_text_from_pdf
from NLP_Engine.experience_extractor import calculate_total_experience, split_resume_into_sections
from typing import Optional, Dict
import re
from NLP_Engine.skill_synonyms import expand_with_domain_bridge


def _extract_projects(text: str, sections: Dict[str, str]) -> Optional[str]:
    """Extract the projects section text from the CV."""
    project_text = sections.get("PROJECTS", "").strip()
    if not project_text:
        # fallback: look for lines after "Projects:" keyword
        match = re.search(r'projects?\s*[:\-]\s*\n(.*?)(?=\n[A-Z][A-Z\s]+:|\Z)',
                          text, re.IGNORECASE | re.DOTALL)
        if match:
            project_text = match.group(1).strip()
    return project_text[:2000] if project_text else None  # cap at 2000 chars


def parse_resume(file_path: str, required_skills):
    text = extract_text_from_pdf(file_path)
    
    # Parse sections first
    sections = split_resume_into_sections(text)

    skill_evidence = extract_skills(text, include_evidence=True)
    extra_evidence = extract_additional_skills(text, include_evidence=True)
    for skill, evidence in extra_evidence.items():
        if skill not in skill_evidence or len(evidence) > len(skill_evidence[skill]):
            skill_evidence[skill] = evidence

    skills = set(normalize_skills(set(skill_evidence.keys())))
    bridged_skills = expand_with_domain_bridge(text.lower())
    skills = skills.union(bridged_skills)
    experience_result = calculate_total_experience(text)
    total_experience = experience_result["years"]
    experience_source = experience_result["source"]

    return {
        "text": text,
        "skills": list(skills),
        "skill_evidence": skill_evidence,
        "total_experience": total_experience,
        "experience_source": experience_source,
        "projects": _extract_projects(text, sections),
    }
