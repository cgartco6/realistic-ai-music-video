from fastapi import APIRouter, Request, HTTPException
from ..models import SessionLocal, VideoJob

router = APIRouter()

@router.post("/sync-labs")
async def sync_labs_webhook(request: Request):
    """Webhook receiver for Sync Labs async completion"""
    data = await request.json()
    job_id = data.get("external_id")
    video_url = data.get("video_url")
    
    db = SessionLocal()
    job = db.query(VideoJob).filter(VideoJob.id == job_id).first()
    if job:
        job.status = "completed"
        job.video_url = video_url
        db.commit()
    db.close()
    return {"status": "received"}
