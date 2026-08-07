from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

import shutil
import os
import random
import hashlib
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

# Serve index.html at root with no-cache headers to prevent browser caching
@app.get("/")
def serve_frontend():
    return FileResponse("index.html", headers={
        "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0"
    })

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
@app.post("/process/")
@app.post("/process")
async def resume_endpoint(request: Request):
    form = await request.form()
    job_text = form.get("job_text", "")
    if isinstance(job_text, UploadFile):
        job_text = ""

    # Extract all uploaded file objects from form across all keys
    raw_files = [v for k, v in form.multi_items() if hasattr(v, "filename") and getattr(v, "filename", None)]
    
    # Deduplicate UploadFile objects by filename and content hash
    upload_list = []
    seen_hashes = set()
    for f_obj in raw_files:
        filename = getattr(f_obj, "filename", None)
        if not filename:
            continue
        file_bytes = await f_obj.read()
        await f_obj.seek(0)
        file_hash = (filename, hashlib.md5(file_bytes).hexdigest())
        if file_hash not in seen_hashes:
            seen_hashes.add(file_hash)
            upload_list.append(f_obj)

    if not upload_list:
        return {"error": "No resume files uploaded. Please select at least one PDF, DOCX, or TXT file."}

    print(f"[Backend] Received {len(upload_list)} uploaded file(s).")
    saved_paths = []
    for idx, file_item in enumerate(upload_list):
        raw_name = getattr(file_item, "filename", None) or f"resume_{idx+1}.pdf"
        base_name = os.path.basename(raw_name)
        safe_name = f"{idx+1}_{base_name}"
        resume_path = os.path.join(UPLOAD_FOLDER, safe_name)

        # Read file byte contents
        file_bytes = await file_item.read()
        if not file_bytes:
            if hasattr(file_item.file, "seek"):
                file_item.file.seek(0)
            file_bytes = file_item.file.read()

        with open(resume_path, "wb") as f:
            f.write(file_bytes)
            
        print(f"[Backend Upload] Saved {safe_name} ({len(file_bytes)} bytes)")
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

    is_written_flag = form.get("is_written")
    interview_mode = form.get("interview_mode")

    # Determine written mode: explicit parameter > duration==2 without audio > false
    if is_written_flag is not None:
        is_written_mode = str(is_written_flag).lower() in ("true", "1", "yes")
    elif interview_mode is not None:
        is_written_mode = (str(interview_mode).lower() == "written")
    else:
        is_written_mode = bool(spoken_text and len(str(spoken_text).strip()) > 0 and audio_file is None and str(form.get("duration", "")) == "2")

    # 1. Computer Vision Camera Gaze & Posture Analysis
    cv_results = analyze_camera(duration=duration, show_preview=False)

    # 2. Speech-to-Text Transcription via Whisper engine with live browser fallback
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