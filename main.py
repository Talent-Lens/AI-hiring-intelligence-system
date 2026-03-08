import os

from NLP_Engine.job_parser import build_job_data
from NLP_Engine.parsers.resume_parser import parse_resume
from NLP_Engine.matcher import match_resume_to_job


def main():

    # ---------------- JOB INPUT ----------------
    job_text = """
   We are looking for a DevOps Engineer to manage infrastructure, automate deployments, and ensure system reliability.
    Responsibilities
    Build and maintain CI/CD pipelines
    Manage cloud infrastructure
    Automate deployment processes
    Monitor system performance and reliability
    Implement containerization and orchestration solutions
    Required Skills
    AWS
    Docker
    Kubernetes
    CI/CD pipelines
    Linux
    Terraform
    Git
    Bash scripting
    Preferred Skills
    Prometheus
    Grafana
    Jenkins
    Microservices architecture
    Infrastructure as Code
"""

    # Build structured job data
    job_data = build_job_data(job_text)

    print("\n--- Job Skill Weights ---")
    for skill, weight in job_data["skill_weights"].items():
        print(f"{skill} : {weight}")
    print("-------------------------\n")

    # ---------------- RESUME FOLDER ----------------
    resume_folder = "resumes"

    if not os.path.exists(resume_folder):
        print(f"Resume folder '{resume_folder}' not found.")
        return

    results = []

    # ---------------- PROCESS RESUMES ----------------
    for filename in os.listdir(resume_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(resume_folder, filename)

        try:
            resume_data = parse_resume(
                file_path,
                required_skills=job_data["required_skills"]
            )

            match_result = match_resume_to_job(job_data, resume_data)

            results.append({
                "filename": filename,
                **match_result,
                "total_experience": resume_data.get("total_experience", 0),
                "skill_experience": resume_data.get("skill_experience", {})
            })

        except Exception as e:
            import traceback
            print(f"\nError processing {filename}")
            traceback.print_exc()

    if not results:
        print("No valid resumes found.")
        return

    # ---------------- SORT RESULTS ----------------
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # ---------------- DISPLAY RESULTS ----------------
    print("\n===== RANKED CANDIDATES =====\n")

    for rank, result in enumerate(results, start=1):

        print(f"Rank #{rank}: {result['filename']}")
        print(f"  Final Score: {result['final_score']*100:.2f}%")
        print(f"  Category: {result['match_category']}")
        print(f"  Base Score (Rule+Semantic): {result['base_score']:.4f}")
        print(f"  Experience Bonus: {result['experience_bonus']:.4f}")
        print(f"  Score Before Penalty: {result['pre_penalty_score']:.4f}")
        print(f"  Rule Score: {result['rule_score']:.4f}")
        print(f"  Semantic Score: {result['semantic_score']:.4f}")
        print(f"  Matched Required: {result['matched_required']}")
        print(f"  Missing Required: {result['missing_required']}")
        semantic_matches = result.get("semantic_skill_matches", {})
        if semantic_matches:
            print("  Semantic Skill Matches:")

            if isinstance(semantic_matches, dict):
                for req, res in semantic_matches.items():
                    print(f"    {req} ← {res}")

        elif isinstance(semantic_matches, list):
            for match in semantic_matches:
                print(f"    {match}")

        print(f"  Total Experience: {result['total_experience']} years")
        print(f"  Skill Experience: {result['skill_experience']}")

        explanation = result.get("explanation", {})

        print("  --- Explanation ---")
        print(f"    Semantic Contribution: {explanation.get('semantic_contribution')}")
        print(f"    Rule Contribution: {explanation.get('rule_contribution')}")
        print(f"    Experience Bonus: {explanation.get('experience_bonus')}")
        print(f"    Mandatory Missing Count: {explanation.get('mandatory_missing_count')}")
        print(f"    Penalty Multiplier: {explanation.get('penalty_multiplier')}")
        
        gap = result["skill_gap_analysis"]

        print("  --- Skill Gap Analysis ---")
        print("    Critical Gaps:", gap["critical_skill_gaps"])
        print("    Moderate Gaps:", gap["moderate_skill_gaps"])
        print("    Minor Gaps:", gap["minor_skill_gaps"])
        print("-" * 60)


if __name__ == "__main__":
    main()