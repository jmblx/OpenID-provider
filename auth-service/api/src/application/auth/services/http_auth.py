from abc import ABC, abstractmethod

from application.auth.token_types import Fingerprint, AccessToken, RefreshToken
from domain.entities.user.model import User
from domain.entities.user.value_objects import RawPassword, Email


class HttpAuthService(ABC):
    """Абстракция для сервиса аутентификации и управления токенами."""

    @abstractmethod
    async def authenticate_user(
        self, email: Email, password: RawPassword, fingerprint: Fingerprint
    ) -> tuple[AccessToken, RefreshToken]:
        """Аутентифицирует пользователя и возвращает токены."""

    @abstractmethod
    async def refresh_access_token(
        self, refresh_token: RefreshToken, fingerprint: Fingerprint
    ) -> AccessToken:
        """Обновляет AccessToken с использованием RefreshToken."""

    @abstractmethod
    async def logout(self, refresh_token: RefreshToken) -> None:
        """Выход пользователя (logout), инвалидация RefreshToken."""
