from NLP_Engine.job_parser import parse_job_description
from NLP_Engine.resume_parser import parse_resume
from NLP_Engine.matcher import match_resume_to_job


def evaluate_resume(job_file, resume_file):
    job_data = parse_job_description(job_file)
    resume_data = parse_resume(resume_file)

    result = match_resume_to_job(job_data, resume_data)

    print(f"\n===== {resume_file} =====")
    print(f"Final Score: {result['final_score']}")
    print(f"Rule Score: {result['rule_score']}")
    print(f"Semantic Score: {result['semantic_score']}")
    print(f"Matched Required: {result['matched_required']}")
    print(f"Missing Required: {result['missing_required']}")


if __name__ == "__main__":
    job_path = "samples/jobs/sample_job.txt"

    resumes = [
        "samples/resumes/resume_strong.txt",
        "samples/resumes/resume_medium.txt",
        "samples/resumes/resume_weak.txt"
    ]

    for resume_path in resumes:
        evaluate_resume(job_path, resume_path)