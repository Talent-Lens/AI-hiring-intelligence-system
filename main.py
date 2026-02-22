from NLP_Engine.resume_parser import parse_resume
from NLP_Engine.job_parser import parse_job_description
from NLP_Engine.matcher import calculate_hybrid_score


resume_path = "samples/resumes/sample_resume.pdf"
job_path = "samples/jobs/sample_job.txt"

resume_data = parse_resume(resume_path)
job_data = parse_job_description(job_path)

def rank_resumes(resume_paths, job_path):
    job_data = parse_job_description(job_path)

    rankings = []

    for path in resume_paths:
        resume_data = parse_resume(path)

        result = calculate_hybrid_score(
            resume_data["text"],
            job_data["text"],
            resume_data["skills"],
            job_data["required_skills"],
            job_data["preferred_skills"]
        )

        rankings.append({
            "resume": path,
            "score": result["final_score"],
            "details": result
        })

    rankings = sorted(rankings, key=lambda x: x["score"], reverse=True)

    return rankings


resumes = [
    "samples/resumes/resume_strong.txt",
    "samples/resumes/resume_weak.txt"
]

ranked = rank_resumes(resumes, "samples/jobs/sample_job.txt")

for r in ranked:
    print("\n=====", r["resume"], "=====")
    print("Score:", r["score"])
    print("Matched Required:", r["details"]["matched_required_skills"])