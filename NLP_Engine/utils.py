import re
import pdfplumber


def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return clean_text(text)


def clean_text(text: str) -> str:
    text = text.replace("\uf0b7", " ")
    text = text.replace("●", " ")
    text = re.sub(r'\s+', ' ', text)
    return text.strip()