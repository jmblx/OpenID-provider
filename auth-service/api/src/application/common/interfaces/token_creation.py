from abc import ABC, abstractmethod

from application.common.token_types import (
    AccessToken,
    Fingerprint,
    RefreshTokenWithData,
)
from domain.entities.user.model import User


class TokenCreationService(ABC):
    """Абстракция для создания токенов."""

    @abstractmethod
    def create_access_token(self, user: User) -> AccessToken:
        """Создание AccessToken."""

    @abstractmethod
    async def create_refresh_token(
        self, user: User, fingerprint: Fingerprint
    ) -> RefreshTokenWithData:
        """Создание RefreshToken."""
