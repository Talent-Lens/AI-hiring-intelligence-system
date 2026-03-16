from fastapi import FastAPI, UploadFile, File
import shutil
import os
import random

from CV_Engine.main import analyze_camera
# from NLP_Engine.resume_score import analyze_resume

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
async def start_interview(resume: UploadFile = File(...)):

    # Save resume
    resume_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Pick random question
    question = random.choice(questions)

    print("Question for candidate:")
    print(question)

    # Run CV engine (20 seconds camera analysis)
    cv_results = analyze_camera(question,20)

    # Run NLP resume scoring
    # resume_score = analyze_resume(resume_path)

    resume_score = 75  # placeholder if NLP not connected yet

    confidence_score = cv_results["confidence_score"]

    final_score = 0.6 * resume_score + 0.4 * confidence_score

    return {
        "question": question,
        "resume_score": resume_score,
        "eye_contact_score": cv_results["eye_contact_score"],
        "head_posture_score": cv_results["head_posture_score"],
        "confidence_score": confidence_score,
        "final_candidate_score": final_score
    }