from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class VideoJob(Base):
    __tablename__ = "video_jobs"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, default="queued")  # queued, processing, completed, failed
    video_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    error_message = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
