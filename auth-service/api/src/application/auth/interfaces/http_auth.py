from abc import ABC, abstractmethod

from application.auth.services.pkce import PKCEData
from application.auth.token_types import Fingerprint, AccessToken, RefreshToken
from domain.entities.user.value_objects import Email, RawPassword


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

    @abstractmethod
    async def authenticate_by_auth_code(
        self,
        auth_code: str,
        redirect_url: str,
        fingerprint: Fingerprint,
        code_challenger: str,
    ) -> tuple[AccessToken, RefreshToken]:
        """Аутентифицирует пользователя по авторизационному коду."""
