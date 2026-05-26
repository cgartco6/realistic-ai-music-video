from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import videos, webhooks

app = FastAPI(title="AI Music Video API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
