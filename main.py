import os

from NLP_Engine.skill_extractor import nlp
from NLP_Engine.parsers.resume_parser import parse_resume
from NLP_Engine.matcher import match_resume_to_job
from NLP_Engine.skill_extractor import extract_skills


# --------------------------------------------------
# BUILD JOB DATA WITH WEIGHTED REQUIRED DETECTION
# --------------------------------------------------

def build_job_data(job_text: str):
    doc = nlp(job_text)

    required_skills = set()
    skill_weights = {}

    for sent in doc.sents:
        sentence_text = sent.text.lower()
        sentence_skills = set(extract_skills(sent.text))

        if not sentence_skills:
            continue

        # Weight detection
        if any(keyword in sentence_text for keyword in ["must", "required", "mandatory"]):
            weight = 3
        elif any(keyword in sentence_text for keyword in ["preferred", "nice to have", "plus"]):
            weight = 1
        else:
            weight = 2  # default medium importance

        for skill in sentence_skills:
            required_skills.add(skill)
            skill_weights[skill] = weight

    return {
        "text": job_text,
        "required_skills": required_skills,
        "skill_weights": skill_weights
    }


# --------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------

def main():

    # -------- JOB INPUT --------
    job_text = """
    We are looking for a Machine Learning Engineer.
    Python and SQL are required.
    Experience with AWS and PyTorch is mandatory.
    Knowledge of NLP is preferred.
    """

    job_data = build_job_data(job_text)

    # -------- RESUME FOLDER --------
    resume_folder = "resumes"

    if not os.path.exists(resume_folder):
        print(f"Resume folder '{resume_folder}' not found.")
        return

    results = []

    for filename in os.listdir(resume_folder):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(resume_folder, filename)

            try:
                resume_data = parse_resume(file_path)
                match_result = match_resume_to_job(job_data, resume_data)

                results.append({
                    "filename": filename,
                    "final_score": match_result["final_score"],
                    "rule_score": match_result["rule_score"],
                    "semantic_score": match_result["semantic_score"],
                    "matched_required": match_result["matched_required"],
                    "missing_required": match_result["missing_required"]
                })

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if not results:
        print("No valid resumes found.")
        return

    # -------- SORT BY FINAL SCORE --------
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # -------- PRINT RANKED RESULTS --------
    print("\n===== RANKED CANDIDATES =====\n")

    for rank, result in enumerate(results, start=1):
        print(f"Rank #{rank}: {result['filename']}")
        print(f"  Final Score: {result['final_score']:.4f}")
        print(f"  Rule Score: {result['rule_score']:.4f}")
        print(f"  Semantic Score: {result['semantic_score']:.4f}")
        print(f"  Matched Required: {result['matched_required']}")
        print(f"  Missing Required: {result['missing_required']}")
        print("-" * 60)


if __name__ == "__main__":
    main()