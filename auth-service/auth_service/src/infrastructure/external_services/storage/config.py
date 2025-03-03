import os

from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class MinIOConfig(BaseModel):
    endpoint_url: str = os.getenv("MINIO_ENDPOINT_URL")
    access_key: str = os.getenv("MINIO_ACCESS_KEY")
    secret_key: str = os.getenv("MINIO_SECRET_KEY")
    user_avatar_bucket_name: str = os.getenv("MINIO_USER_AVATAR_BUCKET_NAME")
    public_url: str = os.getenv("MINIO_PUBLIC_URL")
