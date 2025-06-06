import os
from datetime import timedelta
from io import BytesIO

from PIL import Image
from aiobotocore.session import get_session
from botocore.exceptions import ClientError

from application.common.interfaces.imedia_storage import StorageService
from infrastructure.external_services.storage.config import MinIOConfig


class MinIOService(StorageService):
    def __init__(self, config: MinIOConfig):
        self.config = config
        self.session = get_session()
        self.s3_client = None  # Инициализируется при первом вызове

    async def _get_client(self):
        """Ленивая инициализация клиента (aiobotocore требует async-сессии)."""
        if not self.s3_client:
            self.s3_client = self.session.create_client(
                "s3",
                endpoint_url=self.config.endpoint_url,
                aws_access_key_id=self.config.access_key,
                aws_secret_access_key=self.config.secret_key,
                use_ssl=False,
            )
        return self.s3_client

    def _process_avatar(self, content: bytes) -> bytes:
        """Обрезает и конвертирует изображение в webp (синхронный метод)."""
        with Image.open(BytesIO(content)) as img:
            img = img.convert("RGB")
            img = img.resize((256, 256), Image.LANCZOS)
            output = BytesIO()
            img.save(output, format="WEBP", quality=90)
            return output.getvalue()

    def _get_avatar_filename(self, user_id: str) -> str:
        return f"{user_id}.webp"

    async def set_avatar(self, filename: str, content: bytes, content_type: str, user_id: str) -> str:
        """Загружает аватарку в MinIO (асинхронно)."""
        client = await self._get_client()
        filename = self._get_avatar_filename(user_id)
        try:
            processed_content = self._process_avatar(content)
            await client.put_object(
                Bucket=self.config.user_avatar_bucket_name,
                Key=filename,
                Body=processed_content,
                ContentType="image/webp",
            )
            return await self.get_presigned_avatar_url(user_id)
        except ClientError as e:
            raise Exception(f"Ошибка при загрузке файла в MinIO: {e}")
        finally:
            await client.close()  # Важно закрывать клиент после использования

    async def get_presigned_avatar_url(self, user_id: str) -> str:
        """Генерирует presigned URL для доступа к аватарке (асинхронно)."""
        client = await self._get_client()
        try:
            presigned_url = await client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.config.user_avatar_bucket_name,
                    "Key": self._get_avatar_filename(user_id),
                },
                ExpiresIn=300,  # 5 минут (в секундах)
            )
            presigned_url = presigned_url.replace(
                "minio:9000", os.getenv("HOST_ADDRESS")
            )
            return presigned_url
        except ClientError as e:
            raise Exception(f"Ошибка при генерации presigned URL: {e}")
        finally:
            await client.close()

    async def close(self):
        """Закрывает клиент (вызывайте при завершении работы)."""
        if self.s3_client:
            await self.s3_client.close()