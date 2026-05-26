from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from ..tasks import create_music_video_task
from ..models import SessionLocal, VideoJob
import uuid
import os

router = APIRouter()

@router.post("/generate")
async def generate_video(
    background_tasks: BackgroundTasks,
    audio: UploadFile = File(...),
    source_image: UploadFile = File(...),
    music_url: str = Form(None)
):
    # Validate file types
    if not audio.filename.endswith(('.mp3', '.wav', '.m4a')):
        raise HTTPException(400, "Audio must be MP3, WAV or M4A")
    if not source_image.filename.endswith(('.jpg', '.jpeg', '.png')):
        raise HTTPException(400, "Image must be JPG or PNG")

    job_id = str(uuid.uuid4())
    
    # Save uploaded files temporarily
    audio_path = f"/app/uploads/{job_id}_audio.{audio.filename.split('.')[-1]}"
    image_path = f"/app/uploads/{job_id}_image.{source_image.filename.split('.')[-1]}"
    
    with open(audio_path, "wb") as f:
        f.write(await audio.read())
    with open(image_path, "wb") as f:
        f.write(await source_image.read())

    # Create DB entry
    db = SessionLocal()
    db_job = VideoJob(id=job_id, status="queued")
    db.add(db_job)
    db.commit()
    db.close()

    # Queue task
    background_tasks.add_task(
        create_music_video_task,
        job_id,
        audio_path,
        image_path,
        music_url
    )
    
    return JSONResponse({"job_id": job_id, "status": "queued"})

@router.get("/status/{job_id}")
def get_status(job_id: str):
    db = SessionLocal()
    job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
    db.close()
    if not job:
        raise HTTPException(404, "Job not found")
    return {"job_id": job.id, "status": job.status, "video_url": job.video_url, "error": job.error_message}
