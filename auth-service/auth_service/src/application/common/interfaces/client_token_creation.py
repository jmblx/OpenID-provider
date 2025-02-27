from abc import ABC, abstractmethod
from uuid import UUID

from application.common.auth_server_token_types import (
    Fingerprint,
)
from application.common.client_token_types import ClientAccessToken, ClientRefreshTokenWithData


class ClientTokenCreationService(ABC):
    """Абстракция для создания токенов."""

    @abstractmethod
    def create_client_access_token(
        self, user_id: UUID, user_scopes: list[str]
    ) -> ClientAccessToken:
        """Создание AccessToken."""

    @abstractmethod
    async def create_client_refresh_token(
        self, user_id: UUID, fingerprint: Fingerprint, client_id: int,
    ) -> ClientRefreshTokenWithData:
        """Создание RefreshToken."""
