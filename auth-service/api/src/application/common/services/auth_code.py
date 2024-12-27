import uuid
from abc import ABC, abstractmethod
from typing import Optional, TypedDict


class AuthCodeData(TypedDict):
    user_id: str
    client_id: str
    redirect_url: str
    code_challenger: str


class AuthorizationCodeStorage(ABC):
    @abstractmethod
    async def store_auth_code_data(
        self, auth_code: str, data: AuthCodeData, expiration_time: int = 600
    ) -> None:
        """
        Сохраняет данные, связанные с авторизационным кодом.
        """
        pass

    @abstractmethod
    async def retrieve_auth_code_data(self, auth_code: str) -> Optional[AuthCodeData]:
        """
        Извлекает и удаляет данные, связанные с авторизационным кодом.
        """
        pass

    @abstractmethod
    async def delete_auth_code_data(self, auth_code: str) -> None:
        pass

    def generate_auth_code(self) -> str:
        return str(uuid.uuid4())
