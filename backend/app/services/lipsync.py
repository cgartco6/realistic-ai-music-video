import requests
import subprocess
import os
import time
from ..config import settings

def apply_lipsync(video_path: str, audio_path: str, job_id: str) -> str:
    """
    Use Sync Labs free tier to apply realistic lip-sync.
    Falls back to ffmpeg audio mux if no API key.
    """
    output_video = f"/app/uploads/{job_id}_lipsynced.mp4"

    api_key = settings.SYNC_LABS_API_KEY
    if not api_key:
        # Fallback: just mux audio with video (no lip movement)
        cmd = [
            "ffmpeg", "-i", video_path, "-i", audio_path,
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0",
            "-shortest", output_video
        ]
        subprocess.run(cmd, check=True)
        return output_video

    # Sync Labs API v2 – correct endpoint
    headers = {"x-api-key": api_key}
    files = {
        "video": open(video_path, "rb"),
        "audio": open(audio_path, "rb")
    }
    # Using the documented endpoint
    response = requests.post("https://api.sync.so/v2/lipsync", headers=headers, files=files)
    if response.status_code != 200:
        raise Exception(f"Sync Labs upload failed: {response.text}")
    data = response.json()
    sync_job_id = data["id"]  # note: field name may vary – adjust if needed

    # Poll for completion
    for _ in range(30):
        status_resp = requests.get(f"https://api.sync.so/v2/lipsync/{sync_job_id}", headers=headers)
        if status_resp.status_code != 200:
            continue
        status_data = status_resp.json()
        if status_data.get("status") == "completed":
            video_url = status_data["output"]["video_url"]
            subprocess.run(["curl", "-o", output_video, video_url], check=True)
            return output_video
        time.sleep(2)

    raise Exception("Sync Labs lip-sync timeout")
