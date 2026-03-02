from NLP_Engine.skill_extractor import extract_skills
from NLP_Engine.matcher import match_resume_to_job


def build_job_data(job_text: str):
    from NLP_Engine.skill_extractor import nlp
    doc = nlp(job_text)
    required_skills = set()
    skill_weights = {}

    for sent in doc.sents:
        sentence_text = sent.text.lower()
        sentence_skills = set(extract_skills(sent.text))

        if not sentence_skills:
            continue

        # 🔥 Detect importance level
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


def build_resume_data(resume_text: str):
    resume_skills = set(extract_skills(resume_text))

    return {
        "text": resume_text,
        "skills": resume_skills
    }


if __name__ == "__main__":

    job_text = """
    We are looking for a Machine Learning Engineer.
    Python and SQL are required.
    Experience with AWS and PyTorch is mandatory.
    Knowledge of NLP is preferred.
    """

    resume_text = """
    Experienced in Python, ML, ReactJS, Docker .
    Built NLP pipelines using  deep learning.
    Worked with SQL and MongoDB.
    """

    job_data = build_job_data(job_text)
    resume_data = build_resume_data(resume_text)

    result = match_resume_to_job(job_data, resume_data)

    print("\n===== MATCH RESULT =====\n")
    print("Final Score:", result["final_score"])
    print("Rule Score:", result["rule_score"])
    print("Semantic Score:", result["semantic_score"])
    print("Matched Required:", result["matched_required"])
    print("Missing Required:", result["missing_required"])