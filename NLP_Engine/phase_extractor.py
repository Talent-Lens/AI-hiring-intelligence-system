import spacy
import re

nlp = spacy.load("en_core_web_sm")

STOP_WORDS = {
    "we",
    "our",
    "you",
    "your",
    "build",
    "develop",
    "create",
    "implement",
    "maintain",
    "design",
    "manage",
    "automate",
    "code",
}

STOP_PHRASES = {
    "required skills",
    "preferred skills",
    "responsibilities",
}


def clean_phrase(text):
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def extract_technical_phrases(text):

    doc = nlp(text)
    phrases = []

    for chunk in doc.noun_chunks:

        phrase = clean_phrase(chunk.text)

        words = phrase.split()

        # skip long phrases
        if len(words) > 3:
            continue

        # skip phrases containing stop words
        if any(word in STOP_WORDS for word in words):
            continue

        # skip known section headings
        if phrase in STOP_PHRASES:
            continue

        # skip single letters or very small tokens
        if len(phrase) < 4:
            continue

        phrases.append(phrase)

    return list(set(phrases))