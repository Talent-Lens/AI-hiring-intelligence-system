import re

TECH_PATTERN = r"\b[a-zA-Z0-9\-\+\.#]+\b"

COMMON_TECH_TERMS = {
    "pandas","numpy","scikit-learn","sklearn","tensorflow","keras",
    "pytorch","transformers","bert","gpt","huggingface",
    "docker","kubernetes","spark","hadoop","airflow",
    "postgresql","mongodb","redis",
    "linux","git","github","bash"
}

def extract_additional_skills(text):

    tokens = re.findall(TECH_PATTERN, text.lower())

    detected = set()

    for token in tokens:
        if token in COMMON_TECH_TERMS:
            detected.add(token)

    return detected