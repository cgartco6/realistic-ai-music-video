import boto3
import os
from botocore.config import Config
from ..config import settings

def upload_to_backblaze(file_path: str, object_name: str) -> str:
    """Upload to Backblaze B2 (S3-compatible) and return public URL."""
    session = boto3.Session(
        aws_access_key_id=settings.BACKBLAZE_KEY_ID,
        aws_secret_access_key=settings.BACKBLAZE_APP_KEY,
    )
    s3 = session.client(
        's3',
        endpoint_url='https://s3.us-west-002.backblazeb2.com',
        config=Config(signature_version='s3v4')
    )
    bucket = settings.BACKBLAZE_BUCKET_NAME
    s3.upload_file(file_path, bucket, object_name)
    # Make public (if bucket policy allows)
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=object_name)
    return f"https://f00{settings.BACKBLAZE_KEY_ID}.backblazeb2.com/file/{bucket}/{object_name}"
