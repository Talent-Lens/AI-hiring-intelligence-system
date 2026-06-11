import os
import sys
sys.path.insert(0, os.getcwd())

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

import shutil
import os
import random

from CV_Engine.main import analyze_camera
from main import process_resumes   

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
    return FileResponse(os.path.join(os.getcwd(), "index.html"))

# Mount static files if you have CSS/JS files
app.mount("/static", StaticFiles(directory="static"), name="static")

questions = [
    "Tell me about yourself.",
    "Why should we hire you?",
    "Describe a challenge you solved.",
    "What are your strengths?"
]

from typing import List

@app.post("/resume-scoring/")
async def resume_endpoint(
    resumes: List[UploadFile] = File(...),
    job_text: str = Form(...)
):
    resume_paths = []
    print(f"DEBUG: Received {len(resumes)} resumes.", flush=True)
    
    for resume in resumes:
        print(f"DEBUG: Processing file: {resume.filename}", flush=True)
        # Save resume
        resume_path = os.path.join(UPLOAD_FOLDER, resume.filename)
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        resume_paths.append(resume_path)

    question = random.choice(questions)
    
    # NLP 
    results = process_resumes(job_text, resume_paths)

    if not results:
        print("DEBUG: No results from process_resumes", flush=True)
        return {"error": "Resume processing failed"}

    print(f"DEBUG: Returning {len(results)} results.", flush=True)
    if len(results) > 0:
        res = results[0]
        print(f"DEBUG: First result insights: {res.get('candidate_insights', {}).keys()}", flush=True)
        print(f"DEBUG: First result strengths count: {len(res.get('candidate_insights', {}).get('strengths', []))}", flush=True)

    # We return all results for the frontend to display in ranked order
    return {
        "results": results,
        "question": question,
        "version": "1.0.8"
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