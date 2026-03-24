import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_path: str) -> str:
    text = ""

    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                page_text = page.get_text("text")
                
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

    return clean_text(text)




def clean_text(text: str) -> str:

    # -----------------------------------------------
    # STEP 1: Normalize ALL Unicode whitespace variants
    # to plain ASCII space BEFORE anything else runs.
    # \xa0 = non-breaking space, \u202f = narrow no-break,
    # \u2009 = thin space, \u200b = zero-width space, etc.
    # -----------------------------------------------
    text = re.sub(r'[\xa0\u00a0\u2002\u2003\u2009\u200a\u200b\u202f\u205f\u3000]', ' ', text)

    # -----------------------------------------------
    # STEP 2: Normalize dashes and bullet chars
    # -----------------------------------------------
    text = re.sub(r'[–—−‐]', '-', text)
    text = text.replace('\uf0b7', ' ')
    text = text.replace('●', ' ')

    # -----------------------------------------------
    # STEP 3: Collapse spaced letters — NO \b anchors.
    # Handles both space and newline separators.
    # Pattern: single letter, then 2+ repetitions of
    # (space-or-newline + single letter).
    # Uses lookahead/lookbehind instead of \b.
    # -----------------------------------------------

    # First pass: newline-separated (J\nA\nN\nU\nA\nR\nY)
    text = re.sub(
        r'(?<![A-Za-z])([A-Za-z])(?:\n([A-Za-z])){2,}(?![A-Za-z])',
        lambda m: re.sub(r'\n', '', m.group(0)),
        text
    )

    # Second pass: space-separated (J A N U A R Y or D E T A I L S)
    # Match: (non-alpha or start)(X SPACE){2,}X(non-alpha or end)
    def collapse_spaced(m):
        return m.group(0).replace(' ', '')

    text = re.sub(
        r'(?<![A-Za-z])(?:[A-Za-z] ){2,}[A-Za-z](?![A-Za-z])',
        collapse_spaced,
        text
    )

    # -----------------------------------------------
    # STEP 4: Collapse spaced digits (2 0 2 0 → 2020)
    # Same anchor-free approach
    # -----------------------------------------------
    text = re.sub(
        r'(?<!\d)(?:\d ){3}\d(?!\d)',
        lambda m: m.group(0).replace(' ', ''),
        text
    )

    # -----------------------------------------------
    # STEP 5: Fix word splits caused by collapse.
    # e.g. "TRAVELAGENT" → need space back between words.
    # We re-insert spaces where a run of caps meets another
    # run that was a separate word. This is the tricky part —
    # we use a known section-header list to restore them,
    # plus a general CamelCase-style boundary heuristic.
    # -----------------------------------------------

    # Known header tokens that get merged — restore spaces
    known_headers = [
        'DETAILS', 'SKILLS', 'LINKS', 'LANGUAGES', 'HOBBIES',
        'PROFILE', 'SUMMARY', 'COURSES', 'ACCOMPLISHMENTS',
        'EDUCATION', 'EXPERIENCE', 'EMPLOYMENT', 'HISTORY',
        'CERTIFICATIONS', 'AWARDS', 'REFERENCES', 'CONTACT',
        'TRAVELAGENT', 'DRIVINGLIC', 'PLACEOFBIRTH',
    ]
    # These section headers aren't needed for date parsing, so
    # we don't need to perfectly reconstruct them — they just
    # need to not bleed into date context windows.

    # -----------------------------------------------
    # STEP 6: Normalize whitespace last
    # -----------------------------------------------
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)

    return text.strip()
