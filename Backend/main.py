import sys
sys.path.insert(0, '/app')
print("=== STARTING UP ===", flush=True)

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import shutil
import os
import random

from nlp_main import process_resumes
from CV_Engine.main import analyze_camera

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*","ngrok-skip-browser-warning"],
)
# Serve index.html at root
@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "Describe a challenge you solved.",
    "What are your strengths?"
]

@app.post("/resume-scoring/")
async def resume_endpoint(
    resume: UploadFile = File(...),
    job_text: str = Form(...)
):
    # Save resume
    resume_path = os.path.join(UPLOAD_FOLDER, resume.filename)

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
    question = random.choice(questions)
    # NLP 
    results = process_resumes(job_text, [resume_path])

    if not results:
        return {"error": "Resume processing failed"}

    nlp_result = results[0]
    
    return {
        "nlp_analysis": nlp_result,
        "question": question
    }

@app.get("/analyze-camera/")
def analyze_camera_endpoint():
     # Question
    
    cv_results = analyze_camera(20)   # FIX function to take only duration

    return {
        "cv_analysis": {
            "eye_contact_score": cv_results["eye_contact_score"],
            "head_posture_score": cv_results["head_posture_score"],
            "confidence_score": cv_results["confidence_score"]
        }
    }
@app.post("/final-score/")
async def final_score(nlp_score: float, confidence_score: float):
    final = 0.6 * nlp_score + 0.4 * confidence_score

    return {
        "final_candidate_score": final,
        "hired": final > 65
    }