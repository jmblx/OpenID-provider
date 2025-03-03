from typing import Literal
from uuid import UUID
from redis.asyncio import Redis
import logging

from application.common.interfaces.white_list import TokenWhiteListService
from application.common.auth_server_token_types import (
    RefreshTokenData,
    RefreshTokenWithData,
)

logger = logging.getLogger(__name__)


class TokenWhiteListServiceImpl(TokenWhiteListService):
    """Реализация сервиса управления белым списком токенов с использованием Redis."""

    def __init__(self, redis: Redis, audience: Literal["auth_server", "client"]):
        """
        :param redis: Экземпляр Redis.
        :param audience: Для кого токен (auth_server или client).
        """
        self.redis = redis
        self.audience = audience

    def _serialize_refresh_token_data(self, refresh_token_data: RefreshTokenWithData) -> dict[str, str]:
        """Приводит все поля к сериализуемым в JSON типам (UUID -> str)."""
        return {
            "jti": str(refresh_token_data.jti),
            "user_id": str(refresh_token_data.user_id),
            "fingerprint": refresh_token_data.fingerprint,
            "created_at": refresh_token_data.created_at.isoformat(),
        }

    async def _remove_token_by_jti(self, jti: UUID) -> None:
        """Удаляет токен из всех связанных ключей."""
        token_data = await self.get_refresh_token_data(jti)
        if not token_data:
            logger.warning("Токен с jti %s не найден для удаления.", jti)
            return

        user_id = token_data.user_id

        await self.redis.delete(f"{self.audience}_refresh_token:{jti}")
        await self.redis.zrem(f"{self.audience}_refresh_tokens:{user_id}", jti)

        logger.info("Удалён токен с jti %s из всех связанных ключей.", jti)

    async def is_fingerprint_matching(self, jti: UUID, fingerprint: str) -> bool:
        """Проверяет, совпадает ли переданный fingerprint с fingerprint токена по его jti."""
        token_data = await self.redis.hgetall(f"{self.audience}_refresh_token:{jti}")
        if not token_data:
            logger.warning("Токен с jti: %s не найден", jti)
            return False

        stored_fingerprint = token_data.get("fingerprint")
        if stored_fingerprint is None:
            logger.warning("Fingerprint отсутствует в данных токена с jti: %s", jti)
            return False

        return stored_fingerprint == fingerprint

    async def replace_refresh_token(self, refresh_token_data: RefreshTokenWithData, limit: int) -> None:
        """Сохраняет токен, удаляя старые при необходимости."""
        jti = refresh_token_data.jti
        user_id = refresh_token_data.user_id
        created_at = refresh_token_data.created_at.timestamp()

        num_tokens = await self.redis.zcard(f"{self.audience}_refresh_tokens:{user_id}")
        if num_tokens >= limit:
            oldest_jti_list = await self.redis.zrange(f"{self.audience}_refresh_tokens:{user_id}", 0, 0)
            if oldest_jti_list:
                await self._remove_token_by_jti(oldest_jti_list[0])
        serialized_token_data = self._serialize_refresh_token_data(refresh_token_data)
        logger.info("serialize_refresh_token_data: %s, refresh_token_data: %s", serialized_token_data, refresh_token_data)
        await self.redis.hset(f"{self.audience}_refresh_token:{jti}", mapping=serialized_token_data)
        await self.redis.zadd(f"{self.audience}_refresh_tokens:{user_id}", {jti: created_at})

        logger.info("Сохранён новый токен с jti: %s", jti)

    async def get_refresh_token_data(self, jti: UUID) -> RefreshTokenData | None:
        """Получает данные refresh-токена."""
        token_data = await self.redis.hgetall(f"{self.audience}_refresh_token:{jti}")
        if not token_data:
            return None
        return RefreshTokenData(**token_data)

    async def remove_old_tokens(self, user_id: UUID, fingerprint: str, limit: int) -> None:
        """Удаляет старые токены, если их количество превышает лимит."""
        num_tokens = await self.redis.zcard(f"{self.audience}_refresh_tokens:{user_id}")
        if num_tokens > limit:
            oldest_jti_list = await self.redis.zrange(f"{self.audience}_refresh_tokens:{user_id}", 0, 0)
            if oldest_jti_list:
                oldest_jti = oldest_jti_list[0]
                logger.info("Удаление самого старого токена с jti: %s", oldest_jti)
                await self._remove_token_by_jti(oldest_jti)

    async def remove_token(self, jti: UUID) -> None:
        """Удаляет токен по его JTI."""
        await self._remove_token_by_jti(jti)

    async def remove_tokens_except_current(self, jti: UUID, user_id: UUID) -> None:
        """Удаляет все токены для user_id, кроме указанного jti."""
        token_jtis = await self.redis.zrange(f"{self.audience}_refresh_tokens:{user_id}", 0, -1)

        tokens_to_remove = [token for token in token_jtis if token != str(jti)]

        for token in tokens_to_remove:
            await self._remove_token_by_jti(token)

        if tokens_to_remove:
            await self.redis.zrem(f"{self.audience}_refresh_tokens:{user_id}", *tokens_to_remove)

        logger.info("Удалены все токены, кроме jti: %s", jti)


class AuthServerTokenService(TokenWhiteListServiceImpl):
    """Сервис управления refresh-токенами для auth_server."""

    def __init__(self, redis: Redis):
        super().__init__(redis, "auth_server")


class ClientTokenService(TokenWhiteListServiceImpl):
    """Сервис управления refresh-токенами для client."""

    def __init__(self, redis: Redis):
        super().__init__(redis, "client")
