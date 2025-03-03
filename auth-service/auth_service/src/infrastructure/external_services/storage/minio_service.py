from datetime import timedelta
from io import BytesIO
from urllib.parse import urlunparse, urlparse

from PIL import Image
from minio import Minio
from minio.error import S3Error

from application.common.interfaces.imedia_storage import StorageServiceInterface
from infrastructure.external_services.storage.config import MinIOConfig


class MinIOService(StorageServiceInterface):
    def __init__(self, config: MinIOConfig):
        self.config = config
        self.s3_client = Minio(
            config.endpoint_url,  # Внутри Docker-сети используйте имя контейнера
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=False  # Используйте True, если MinIO настроен с TLS
        )

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

    def _get_avatar_filename(self, user_id: str) -> str:
        return f"{user_id}.webp"

    def set_avatar(self, filename: str, content: bytes, content_type: str, user_id: str) -> str:
        """
        Загружает аватарку в MinIO.
        """
        filename = f"{user_id}.webp"
        try:
            processed_content = self._process_avatar(content)
            self.s3_client.put_object(
                self.config.user_avatar_bucket_name,  # Бакет
                filename,  # Имя файла
                BytesIO(processed_content),
                length=len(processed_content),
                content_type="image/webp"
            )
            return self.get_presigned_avatar_url(user_id)
        except S3Error as e:
            raise Exception(f"Ошибка при загрузке файла в MinIO: {e}")


    def get_presigned_avatar_url(self, user_id: str) -> str:
        """
        Генерирует presigned URL для доступа к аватарке.
        Заменяет хост в URL на public_url.
        """
        try:
            # Генерируем presigned URL
            presigned_url = self.s3_client.presigned_get_object(
                self.config.user_avatar_bucket_name,
                self._get_avatar_filename(user_id),  # Имя файла
                expires=timedelta(minutes=5)
            )
            #
            # # Разбираем URL на компоненты
            # parsed_url = urlparse(presigned_url)
            #
            # # Заменяем хост и порт на public_url
            # new_netloc = self.config.public_url
            # if ":" in new_netloc:
            #     new_netloc = new_netloc.split(":")[0]  # Убираем порт, если он есть
            #
            # # Собираем новый URL
            # new_url = parsed_url._replace(netloc=new_netloc)
            # presigned_url = urlunparse(new_url)
            presigned_url = presigned_url.replace("minio:9000", "minio.example.com")

            return presigned_url
        except S3Error as e:
            raise Exception(f"Ошибка при генерации presigned URL: {e}")