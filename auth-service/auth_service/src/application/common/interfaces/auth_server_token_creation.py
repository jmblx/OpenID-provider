from abc import ABC, abstractmethod
from uuid import UUID

from application.common.auth_server_token_types import (
    AccessToken,
    Fingerprint,
    RefreshTokenWithData,
)
from domain.entities.user.model import User


class AuthServerTokenCreationService(ABC):
    """Абстракция для создания токенов."""

    @abstractmethod
    def create_auth_server_access_token(
        self, user_id: UUID
    ) -> AccessToken:
        """Создание AccessToken."""

    @abstractmethod
    async def create_auth_server_refresh_token(
        self, user_id: UUID, fingerprint: Fingerprint
    ) -> RefreshTokenWithData:
        """Создание RefreshToken."""
