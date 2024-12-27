from abc import ABC, abstractmethod
from uuid import UUID
from application.common.token_types import RefreshTokenWithData


class TokenWhiteListService(ABC):
    """Абстракция для управления токенами (например, белый список)."""

    @abstractmethod
    async def is_fingerprint_matching(self, jti: UUID, fingerprint: str) -> bool:
        """Проверка соответствия отпечатка refresh токена."""

    @abstractmethod
    async def save_refresh_token(
        self, refresh_token_data: RefreshTokenWithData, limit: int
    ) -> None:
        """Сохранение RefreshToken."""

    @abstractmethod
    async def get_refresh_token_data(self, jti: UUID) -> RefreshTokenWithData:
        """Получение данных RefreshToken по JTI."""

    @abstractmethod
    async def remove_old_tokens(
        self, user_id: UUID, fingerprint: str, limit: int
    ) -> None:
        """Удаление старых токенов, если превышен лимит."""

    @abstractmethod
    async def remove_token(self, jti: UUID) -> None:
        """Удаление токена по его JTI."""

    @abstractmethod
    async def get_existing_jti(self, user_id: UUID, fingerprint: str) -> str | None:
        """Получение существующего JTI для пользователя по fingerprint."""

    @abstractmethod
    async def remove_tokens_except_current(self, jti: UUID, user_id: UUID) -> None:
        """Удаление всех токенов, кроме текущего."""
