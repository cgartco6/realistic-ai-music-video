from celery import Celery
from .config import settings
from .services.music_source import extract_audio_from_url, save_uploaded_audio
from .services.avatar_animation import animate_avatar
from .services.lipsync import apply_lipsync
from .services.storage import upload_to_backblaze
from .models import SessionLocal, VideoJob
import os
import logging

celery_app = Celery('tasks', broker=settings.REDIS_URL)
celery_app.conf.update(task_track_started=True)

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def create_music_video_task(self, job_id: str, audio_path: str, image_path: str, music_url: str = None):
    db = SessionLocal()
    try:
        # Update status to processing
        db.query(VideoJob).filter(VideoJob.id == job_id).update({"status": "processing"})
        db.commit()

        # Step 1: Get final audio file
        if music_url:
            final_audio = extract_audio_from_url(music_url, job_id)
        else:
            final_audio = audio_path

        # Step 2: Animate avatar (full body)
        animated_video = animate_avatar(image_path, final_audio, job_id)
        if not animated_video:
            raise Exception("Avatar animation failed")

        # Step 3: Apply lip-sync
        synced_video = apply_lipsync(animated_video, final_audio, job_id)
        if not synced_video:
            raise Exception("Lip-sync failed")

        # Step 4: Upload to free cloud storage
        video_url = upload_to_backblaze(synced_video, f"{job_id}.mp4")

        # Step 5: Update database
        db.query(VideoJob).filter(VideoJob.id == job_id).update({
            "status": "completed",
            "video_url": video_url
        })
        db.commit()

        # Cleanup temporary files
        for f in [audio_path, image_path, final_audio, animated_video, synced_video]:
            if f and os.path.exists(f):
                os.remove(f)

    except Exception as e:
        logger.exception(f"Job {job_id} failed")
        db.query(VideoJob).filter(VideoJob.id == job_id).update({
            "status": "failed",
            "error_message": str(e)
        })
        db.commit()
    finally:
        db.close()
