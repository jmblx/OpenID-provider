from abc import ABC, abstractmethod
from uuid import UUID
from application.auth.token_types import RefreshTokenData
from domain.entities.user.value_objects import UserID


class TokenWhiteListService(ABC):
    """Абстракция для управления токенами (например, белый список)."""

    @abstractmethod
    async def save_refresh_token(
        self, refresh_token_data: RefreshTokenData
    ) -> None:
        """Сохранение RefreshToken."""

    @abstractmethod
    async def get_refresh_token_data(self, jti: UUID) -> RefreshTokenData:
        """Получение данных RefreshToken по JTI."""

    @abstractmethod
    async def remove_old_tokens(
        self, user_id: UserID, fingerprint: str, limit: int
    ) -> None:
        """Удаление старых токенов, если превышен лимит."""

    @abstractmethod
    async def remove_token(self, jti: UUID) -> None:
        """Удаление токена по его JTI."""

    @abstractmethod
    async def get_existing_jti(
        self, user_id: UserID, fingerprint: str
    ) -> str | None:
        """Получение существующего JTI для пользователя по fingerprint."""
