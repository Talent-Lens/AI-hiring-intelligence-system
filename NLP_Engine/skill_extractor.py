import spacy
from spacy.matcher import PhraseMatcher

# Load model once
nlp = spacy.load("en_core_web_sm")

# Canonical skill dictionary (normalized form)
SKILL_DB = {
    "python": ["python"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "natural language processing": ["nlp", "natural language processing"],
    "c++": ["c++"],
    "java": ["java"],
    "sql": ["sql"],
    "mongodb": ["mongodb"],
    "react": ["react", "reactjs"],
    "node.js": ["node.js", "nodejs"],
    "django": ["django"],
    "flask": ["flask"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes"],
    "git": ["git"]
}

# Build matcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

for canonical, variations in SKILL_DB.items():
    patterns = [nlp.make_doc(text) for text in variations]
    matcher.add(canonical, patterns)


def extract_skills(text: str):
    doc = nlp(text)
    matches = matcher(doc)

    extracted = set()

    for match_id, start, end in matches:
        skill_name = nlp.vocab.strings[match_id]
        extracted.add(skill_name)

    return list(extracted)