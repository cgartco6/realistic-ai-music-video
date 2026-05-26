import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN", "")
    SYNC_LABS_API_KEY = os.getenv("SYNC_LABS_API_KEY", "")
    BACKBLAZE_KEY_ID = os.getenv("BACKBLAZE_KEY_ID", "")
    BACKBLAZE_APP_KEY = os.getenv("BACKBLAZE_APP_KEY", "")
    BACKBLAZE_BUCKET_NAME = os.getenv("BACKBLAZE_BUCKET_NAME", "ai-music-videos")
    USE_LOCAL_AVATAR = os.getenv("USE_LOCAL_AVATAR", "true").lower() == "true"
    LOCAL_MODELS_PATH = os.getenv("LOCAL_MODELS_PATH", "/app/models")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    YOUTUBE_DL_PATH = os.getenv("YOUTUBE_DL_PATH", "yt-dlp")

settings = Settings()
