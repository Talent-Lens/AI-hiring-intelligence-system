import os

from NLP_Engine.job_parser import build_job_data
from NLP_Engine.parsers.resume_parser import parse_resume
from NLP_Engine.matcher import match_resume_to_job
from NLP_Engine.skill_gap_analyzer import analyze_skill_gap
from NLP_Engine.explanation_engine import generate_candidate_insights   


def process_resumes(job_text: str, resume_files: list):
    
    job_data = build_job_data(job_text)
    results = []

    for file_path in resume_files:
        try:
            resume_data = parse_resume(
                file_path,
                required_skills=job_data["required_skills"]
            )

            match_result = match_resume_to_job(job_data, resume_data)
            skill_gap = analyze_skill_gap(job_data, resume_data)
            insights = generate_candidate_insights(match_result, skill_gap)

            results.append({
                "filename": os.path.basename(file_path),
                **match_result,
                "total_experience": resume_data.get("total_experience", 0),
                "skill_gap_analysis": skill_gap,
                "candidate_insights": insights
            })

        except Exception as e:
            import traceback
            print(f"Error processing {file_path}")
            traceback.print_exc()

    if not results:
        return []

    # sort
    results.sort(key=lambda x: x["final_score"], reverse=True)

    return results