import re

TECH_PATTERN = r"\b[a-zA-Z0-9\-\+\.#]+\b"

COMMON_TECH_TERMS = {
    "pandas","numpy","scikit-learn","sklearn","tensorflow","keras",
    "pytorch","transformers","bert","gpt","huggingface",
    "docker","kubernetes","spark","hadoop","airflow",
    "postgresql","mongodb","redis",
    "linux","git","github","bash"
}

def extract_additional_skills(text: str, include_evidence: bool = False):
    if not include_evidence:
        tokens = re.findall(TECH_PATTERN, text.lower())
        detected = set()
        for token in tokens:
            if token in COMMON_TECH_TERMS:
                detected.add(token)
        return detected

    skill_evidence = {}
    
    # Split text into sentences and lines for context
    sentences = re.split(r'(?<=[.!?])\s+', text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    for sentence in sentences:
        clean_sentence = " ".join(sentence.split())
        tokens = re.findall(TECH_PATTERN, clean_sentence.lower())
        for token in tokens:
            if token in COMMON_TECH_TERMS:
                # Try to narrow down to a single line if the sentence is too long
                best_evidence = clean_sentence
                for line in lines:
                    if token in line.lower() and len(line) < len(best_evidence):
                        best_evidence = line
                
                if token not in skill_evidence or len(best_evidence) > len(skill_evidence[token]):
                    skill_evidence[token] = best_evidence

                    
    return skill_evidence