import uuid
from abc import ABC, abstractmethod
from typing import Optional, TypedDict, Literal, get_args

from domain.entities.resource_server.value_objects import ResourceServerIds


UserScope = Literal["email", "avatar_path"]
ALLOWED_SCOPES: list[str] = list(get_args(UserScope))


class AuthCodeData(TypedDict, total=False):
    user_id: str
    client_id: str
    code_challenger: str
    user_data_needed: list[UserScope]
    rs_ids: ResourceServerIds


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
    async def retrieve_auth_code_data(
        self, auth_code: str
    ) -> Optional[AuthCodeData]:
        """
        Извлекает и удаляет данные, связанные с авторизационным кодом.
        """
        pass

    @abstractmethod
    async def delete_auth_code_data(self, auth_code: str) -> None:
        pass

    def generate_auth_code(self) -> str:
        return str(uuid.uuid4())
