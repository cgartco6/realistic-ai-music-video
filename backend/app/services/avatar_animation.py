import replicate
import subprocess
import os
from ..config import settings

def animate_avatar(image_path: str, audio_path: str, job_id: str) -> str:
    """
    Generate full-body animation from image and audio.
    Uses local OmniAvatar if USE_LOCAL_AVATAR=true, otherwise Replicate's OmniHuman.
    """
    output_video = f"/app/uploads/{job_id}_animated.mp4"

    if settings.USE_LOCAL_AVATAR:
        # Assume OmniAvatar is installed at /app/models/OmniAvatar
        # This is a placeholder – you would replace with actual local inference
        # For demo, we just copy the image as a static video with audio
        cmd = [
            "ffmpeg", "-loop", "1", "-i", image_path,
            "-i", audio_path,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
            "-shortest", output_video
        ]
        subprocess.run(cmd, check=True)
    else:
        # Use Replicate's OmniHuman model (free credits)
        replicate.client.api_token = settings.REPLICATE_API_TOKEN
        input = {
            "image": open(image_path, "rb"),
            "audio": open(audio_path, "rb")
        }
        output = replicate.run(
            "bytedance/omni-human-1.5:latest",
            input=input
        )
        # Download the output video
        subprocess.run(["curl", "-o", output_video, output], check=True)

    return output_video
