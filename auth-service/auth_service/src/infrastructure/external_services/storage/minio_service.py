import os
import time
from datetime import timedelta
from io import BytesIO

from PIL import Image
from minio import Minio
from minio.error import S3Error
from redis.asyncio import Redis

from application.common.interfaces.imedia_storage import StorageService
from infrastructure.external_services.storage.config import MinIOConfig


class MinIOService(StorageService):
    def __init__(self, config: MinIOConfig, bucket_name: str, redis: Redis):
        self.config = config
        self.s3_client = Minio(
            config.endpoint_url,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=False
        )
        self.bucket_name = bucket_name
        self.redis = redis

    def _process_avatar(self, content: bytes) -> bytes:
        """
        Обрезает и конвертирует изображение в webp.
        """
        with Image.open(BytesIO(content)) as img:
            img = img.convert("RGB")
            img = img.resize((256, 256), Image.LANCZOS)
            output = BytesIO()
            img.save(output, format="WEBP", quality=90)
            return output.getvalue()

    def _get_avatar_filename(self, object_id: str) -> str:
        return f"{object_id}.webp"

    def set_avatar(self, content: bytes, content_type: str, object_id: str) -> str:
        """
        Загружает аватарку в MinIO.
        """
        filename = f"{object_id}.webp"
        try:
            processed_content = self._process_avatar(content)
            self.s3_client.put_object(
                self.bucket_name,  # Бакет
                filename,  # Имя файла
                BytesIO(processed_content),
                length=len(processed_content),
                content_type="image/webp"
            )
            self.redis.set(f"user_avatar:{object_id}", int(time.time()))
            return self.get_presigned_avatar_url(object_id)
        except S3Error as e:
            raise Exception(f"Ошибка при загрузке файла в MinIO: {e}")

    def get_presigned_avatar_url(self, object_id: str) -> str:
        """
        Генерирует presigned URL для доступа к аватарке.
        Заменяет хост в URL на public_url.
        """
        try:
            presigned_url = self.s3_client.presigned_get_object(
                self.bucket_name,
                self._get_avatar_filename(object_id),
                expires=timedelta(minutes=5)
            )
            presigned_url = presigned_url.replace("minio:9000", os.getenv("HOST_ADDRESS"))

            return presigned_url
        except S3Error as e:
            raise Exception(f"Ошибка при генерации presigned URL: {e}")
