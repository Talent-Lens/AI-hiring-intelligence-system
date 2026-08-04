import os
import re

from NLP_Engine.job_parser import build_job_data
from NLP_Engine.parsers.resume_parser import parse_resume
from NLP_Engine.matcher import match_resume_to_job
from NLP_Engine.skill_gap_analyzer import analyze_skill_gap
from NLP_Engine.explanation_engine import generate_candidate_insights   


def process_resumes(job_text: str, resume_files: list):
    
    job_data = build_job_data(job_text)
    results = []

    print(f"[NLP Engine] Processing {len(resume_files)} resume file(s)...")
    for file_path in resume_files:
        try:
            resume_data = parse_resume(
                file_path,
                required_skills=job_data["required_skills"]
            )

            match_result = match_resume_to_job(job_data, resume_data)
            skill_gap = analyze_skill_gap(job_data, resume_data)
            insights = generate_candidate_insights(match_result, skill_gap)

            clean_filename = re.sub(r'^\d+_', '', os.path.basename(file_path))
            results.append({
                "filename": clean_filename,
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

    # Sort candidates by final_score in descending order
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # Assign fair rank position, relative percentile, and fairness metrics
    total_candidates = len(results)
    for idx, candidate in enumerate(results):
        candidate["rank"] = idx + 1
        candidate["total_candidates"] = total_candidates
        if total_candidates > 1:
            # Fair relative percentile ranking
            candidate["percentile"] = round(((total_candidates - idx) / total_candidates) * 100, 1)
        else:
            candidate["percentile"] = 100.0

    return results