from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    def set_avatar(self, filename: str, content: bytes, content_type: str, user_id: str) -> str:
        """
        Загружает файл в указанный бакет.

        :param bucket_name: Название бакета
        :param filename: Имя файла в бакете
        :param content: Содержимое файла в байтах
        :param content_type: MIME-тип содержимого файла
        :param user_id: тот кому принадлежит аватар новый
        :return: URL загруженного файла
        """

    @abstractmethod
    def get_presigned_avatar_url(self, filename: str) -> str: ...
