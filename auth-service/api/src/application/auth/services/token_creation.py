from abc import ABC, abstractmethod

from application.auth.token_types import (
    AccessToken,
    Fingerprint,
    RefreshTokenData,
)
from domain.entities.user.model import User


class TokenCreationService(ABC):
    """Абстракция для создания токенов."""

    @abstractmethod
    def create_access_token(self, user: User) -> AccessToken:
        """Создание AccessToken."""

    @abstractmethod
    def create_refresh_token(
        self, user: User, fingerprint: Fingerprint
    ) -> RefreshTokenData:
        """Создание RefreshToken."""
