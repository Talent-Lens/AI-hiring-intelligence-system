import os

from NLP_Engine.job_parser import build_job_data
from NLP_Engine.parsers.resume_parser import parse_resume
from NLP_Engine.matcher import match_resume_to_job
from NLP_Engine.skill_gap_analyzer import analyze_skill_gap
from NLP_Engine.explanation_engine import generate_candidate_insights   


def process_resumes(job_text: str, resume_files: list):
    
    job_data = build_job_data(job_text)
    results = []

    for i, file_path in enumerate(resume_files):
        print(f"DEBUG: Processing resume {i+1}/{len(resume_files)}: {file_path}", flush=True)
        try:
            resume_data = parse_resume(
                file_path,
                required_skills=job_data["required_skills"]
            )
            print(f"DEBUG: Parsed {file_path} successfully.", flush=True)

            match_result = match_resume_to_job(job_data, resume_data)
            skill_gap = match_result.get("skill_gap_analysis", {})
            insights = match_result.get("candidate_insights", {})

            results.append({
                "filename": os.path.basename(file_path),
                **match_result,
                "total_experience": resume_data.get("total_experience", 0),
            })
            print(f"DEBUG: Added {file_path} to results with score {match_result.get('final_score')}", flush=True)

        except Exception as e:
            print(f"ERROR: Failed to process {file_path}: {str(e)}", flush=True)
            import traceback
            traceback.print_exc()

    if not results:
        return []

    # sort
    results.sort(key=lambda x: x["final_score"], reverse=True)

    return results