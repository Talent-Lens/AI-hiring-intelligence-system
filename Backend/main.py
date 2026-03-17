from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
import random

from CV_Engine.main import analyze_camera
from main import process_resumes   

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "Describe a challenge you solved.",
    "What are your strengths?"
]


@app.post("/start-interview/")
async def start_interview(
    resume: UploadFile = File(...),
    job_text: str = Form(...)
):

    # ---------------- SAVE RESUME ----------------
    resume_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # ---------------- QUESTION ----------------
    question = random.choice(questions)

    # ---------------- CV ENGINE ----------------
    cv_results = analyze_camera(question, 20)   

    # ---------------- NLP ENGINE ----------------
    results = process_resumes(job_text, [resume_path])

    if not results:
        return {"error": "Resume processing failed"}

    nlp_result = results[0]

    # ---------------- FINAL SCORE ----------------
    confidence_score = cv_results["confidence_score"]

    

    return {
    "question": question,

    # -------- NLP FULL OUTPUT --------
    "nlp_analysis": nlp_result,

    # -------- CV OUTPUT --------
    "cv_analysis": {
        "eye_contact_score": cv_results["eye_contact_score"],
        "head_posture_score": cv_results["head_posture_score"],
        "confidence_score": cv_results["confidence_score"]
    },

    # -------- FINAL SCORE --------
    "final_candidate_score": 0.6 * nlp_result["final_score"] + 0.4 * cv_results["confidence_score"]
}