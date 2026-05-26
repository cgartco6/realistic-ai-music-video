import subprocess
import os
from ..config import settings

def extract_audio_from_url(url: str, job_id: str) -> str:
    """Download audio from Suno, aimusic.so, YouTube etc. using yt-dlp"""
    output_path = f"/app/uploads/{job_id}_extracted_audio.mp3"
    cmd = [
        settings.YOUTUBE_DL_PATH,
        "--extract-audio",
        "--audio-format", "mp3",
        "--output", output_path,
        url
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path

def save_uploaded_audio(uploaded_path: str) -> str:
    """Just return the already saved path"""
    return uploaded_path
