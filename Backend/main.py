from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

import shutil
import os
import random
from typing import List, Optional

from CV_Engine.main import analyze_camera
from CV_Engine.audio_transcriber import transcribe_audio_file
from CV_Engine.interview_evaluator import (
    generate_interview_question,
    evaluate_spoken_answer,
    calculate_multifactor_verdict
)
from main import process_resumes   

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# For frontend connection
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

# Mount static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

questions = [
    "Tell me about yourself and walk us through your key technical projects.",
    "Why are you interested in this role and what makes you a strong fit?",
    "Describe a challenging architectural problem you encountered and how you solved it.",
    "How do you handle performance optimization, scaling, and database design?"
]

@app.post("/resume-scoring/")
async def resume_endpoint(request: Request):
    form = await request.form()
    job_text = form.get("job_text", "")
    if isinstance(job_text, UploadFile):
        job_text = ""

    # Extract all uploaded file objects from multipart form
    upload_list = []
    seen_filenames = set()
    for key, value in form.multi_items():
        if hasattr(value, "filename") and getattr(value, "filename", None):
            fname = value.filename
            if fname not in seen_filenames:
                seen_filenames.add(fname)
                upload_list.append(value)

    if not upload_list:
        return {"error": "No resume files uploaded. Please select at least one PDF, DOCX, or TXT file."}

    saved_paths = []
    for file_item in upload_list:
        resume_path = os.path.join(UPLOAD_FOLDER, file_item.filename)
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(file_item.file, buffer)
        saved_paths.append(resume_path)

    if not saved_paths:
        return {"error": "No valid resume files processed."}

    # Process all resumes through upgraded NLP Engine
    results = process_resumes(job_text, saved_paths)

    if not results:
        return {"error": "Resume processing failed"}

    top_cand = results[0]
    domain = top_cand.get("summary", {}).get("domain", "Engineering")
    cand_skills = list(top_cand.get("demonstrated_skills", {}).keys()) or top_cand.get("matched_required", [])
    dynamic_q = generate_interview_question(domain, cand_skills)

    return {
        "results": results,
        "ranked_candidates": results,
        "top_candidate": top_cand,
        "total_candidates": len(results),
        "nlp_analysis": top_cand,
        "question": dynamic_q
    }

@app.get("/analyze-camera/")
@app.post("/analyze-video-interview/")
async def analyze_video_interview_endpoint(request: Request):
    form = await request.form()
    audio_file = form.get("audio")
    spoken_text = form.get("spoken_text", "")
    duration = int(form.get("duration", 15))
    resume_score = float(form.get("resume_score", 0.75))
    question_text = str(form.get("question_text", "Describe a technical challenge you solved."))

    audio_path = None
    if hasattr(audio_file, "file"):
        audio_path = os.path.join(UPLOAD_FOLDER, "candidate_interview_audio.webm")
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

    # 1. Computer Vision Camera Gaze & Posture Analysis
    cv_results = analyze_camera(duration=duration, show_preview=False)

    # 2. Speech-to-Text Transcription via Whisper engine with live browser fallback
    is_written_mode = bool(spoken_text and len(str(spoken_text).strip()) > 0 and audio_file is None)
    if is_written_mode:
        words = str(spoken_text).strip().split()
        stt_results = {
            "transcript": str(spoken_text).strip(),
            "word_count": len(words),
            "wpm": 135.0,
            "pace_rating": "Written Candidate Response",
            "transcription_accuracy": 100.0
        }
        cv_results["confidence_score"] = 85.0
    else:
        stt_results = transcribe_audio_file(audio_path, fallback_text=spoken_text)

    # 3. Evaluate Spoken/Written Answer against Technical Question
    answer_eval = evaluate_spoken_answer(question_text, stt_results["transcript"])

    # 4. Aggregate Multi-Factor Signals (Resume + Spoken Answer + CV Visual)
    multifactor = calculate_multifactor_verdict(
        resume_nlp_score=resume_score,
        spoken_answer_score=answer_eval["spoken_answer_score"],
        visual_confidence_score=cv_results["confidence_score"],
        is_written_mode=is_written_mode
    )

    return {
        "cv_analysis": cv_results,
        "speech_transcription": stt_results,
        "spoken_evaluation": answer_eval,
        "multifactor_verdict": multifactor
    }

@app.post("/final-score/")
async def final_score(nlp_score: float, confidence_score: float, spoken_score: Optional[float] = 0.75):
    res = calculate_multifactor_verdict(
        resume_nlp_score=nlp_score,
        spoken_answer_score=spoken_score,
        visual_confidence_score=confidence_score
    )
    return res