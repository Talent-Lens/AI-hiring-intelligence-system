from NLP_Engine.resume_parser import parse_resume
from NLP_Engine.job_parser import parse_job_description
from NLP_Engine.matcher import calculate_rule_score


resume_path = "samples/resumes/sample_resume.pdf"
job_path = "samples/jobs/sample_job.txt"

resume_data = parse_resume(resume_path)
job_data = parse_job_description(job_path)

score = calculate_rule_score(resume_data["skills"], job_data["skills"])

print("Resume Skills:", resume_data["skills"])
print("Job Skills:", job_data["skills"])
print("Match Score:", score)