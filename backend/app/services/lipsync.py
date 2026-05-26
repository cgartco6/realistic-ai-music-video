import requests
import subprocess
import os
import time
from ..config import settings

def apply_lipsync(video_path: str, audio_path: str, job_id: str) -> str:
    """
    Use Sync Labs free tier to apply realistic lip-sync.
    Returns path to final video.
    """
    output_video = f"/app/uploads/{job_id}_lipsynced.mp4"

    # Sync Labs API – free 3 videos per month
    api_key = settings.SYNC_LABS_API_KEY
    if not api_key:
        # Fallback: use Wav2Lip locally (you'd need to install it)
        # For this demo, we just mux audio with video (no lip movement)
        cmd = [
            "ffmpeg", "-i", video_path, "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0",
            "-shortest", output_video
        ]
        subprocess.run(cmd, check=True)
        return output_video

    # Upload video and audio to Sync Labs
    headers = {"x-api-key": api_key}
    files = {
        "video": open(video_path, "rb"),
        "audio": open(audio_path, "rb")
    }
    response = requests.post("https://api.sync.so/v2/lipsync", headers=headers, files=files)
    data = response.json()
    job_id_sync = data["job_id"]

    # Poll for completion (free tier is synchronous enough)
    for _ in range(30):
        status_resp = requests.get(f"https://api.sync.so/v2/lipsync/{job_id_sync}", headers=headers)
        status_data = status_resp.json()
        if status_data["status"] == "completed":
            video_url = status_data["video_url"]
            # Download the result
            subprocess.run(["curl", "-o", output_video, video_url], check=True)
            return output_video
        time.sleep(2)

    raise Exception("Sync Labs lip-sync timeout")
