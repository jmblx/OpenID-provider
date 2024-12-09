import logging
from typing import Optional, Any
from uuid import UUID

from redis.asyncio import Redis
from application.auth.interfaces.white_list import TokenWhiteListService
from application.auth.token_types import RefreshTokenWithData, RefreshTokenData

logger = logging.getLogger(__name__)


class TokenWhiteListServiceImpl(TokenWhiteListService):
    """Реализация сервиса управления белым списком токенов с использованием Redis."""

    def __init__(self, redis: Redis):
        self.redis = redis

    def _serialize_refresh_token_data(
        self, refresh_token_data: RefreshTokenWithData
    ) -> dict[str, str]:
        """Приводит все поля к типам, которые можно сериализовать в JSON (UUID -> str)."""
        return {
            "jti": str(refresh_token_data.jti),
            "user_id": str(refresh_token_data.user_id),
            "fingerprint": refresh_token_data.fingerprint,
            "created_at": refresh_token_data.created_at.isoformat(),
        }

    async def remove_token_by_jti(self, jti: UUID) -> None:
        """Удаляет токен из всех связанных ключей."""
        token_data = await self.get_refresh_token_data(jti)
        if not token_data:
            logger.warning("Токен с jti %s не найден для удаления.", jti)
            return

        user_id = token_data.user_id
        fingerprint = token_data.fingerprint

        await self.redis.delete(f"refresh_token:{jti}")
        await self.redis.zrem(f"refresh_tokens:{user_id}", jti)
        await self.redis.delete(f"refresh_token_index:{user_id}:{fingerprint}")
        logger.info("Удалён токен с jti %s из всех связанных ключей.", jti)

    async def save_refresh_token(
        self, refresh_token_data: RefreshTokenWithData, limit: int
    ) -> None:
        """Сохраняет токен, удаляя старые при необходимости."""
        jti = refresh_token_data.jti
        user_id = refresh_token_data.user_id
        fingerprint = refresh_token_data.fingerprint
        created_at = refresh_token_data.created_at.timestamp()

        # Удаление существующего токена для данного user_id и fingerprint
        existing_jti = await self.get_existing_jti(user_id, fingerprint)
        if existing_jti:
            await self.remove_token_by_jti(existing_jti)

        # Удаление самых старых токенов, если превышен лимит
        num_tokens = await self.redis.zcard(f"refresh_tokens:{user_id}")
        if num_tokens >= limit:
            oldest_jti_list = await self.redis.zrange(f"refresh_tokens:{user_id}", 0, 0)
            if oldest_jti_list:
                await self.remove_token_by_jti(oldest_jti_list[0])

        # Сохранение нового токена
        serialized_token_data = self._serialize_refresh_token_data(refresh_token_data)
        await self.redis.hset(f"refresh_token:{jti}", mapping=serialized_token_data)
        await self.redis.set(f"refresh_token_index:{user_id}:{fingerprint}", jti)
        await self.redis.zadd(f"refresh_tokens:{user_id}", {jti: created_at})
        logger.info("Сохранён новый токен с jti: %s", jti)

    async def get_refresh_token_data(self, jti: UUID) -> Optional[RefreshTokenData]:
        token_data = await self.redis.hgetall(f"refresh_token:{jti}")
        if not token_data:
            return None
        return RefreshTokenData(**token_data)

    async def remove_old_tokens(
        self, user_id: UUID, fingerprint: str, limit: int
    ) -> None:
        num_tokens = await self.redis.zcard(f"refresh_tokens:{user_id}")
        if num_tokens > limit:
            oldest_jti_list = await self.redis.zrange(f"refresh_tokens:{user_id}", 0, 0)
            if oldest_jti_list:
                oldest_jti = oldest_jti_list[0]
                logger.info("Удаление самого старого токена с jti: %s", oldest_jti)
                await self.redis.zrem(f"refresh_tokens:{user_id}", oldest_jti)
                await self.redis.delete(f"refresh_token:{oldest_jti}")
                await self.redis.delete(f"refresh_token_index:{user_id}:{fingerprint}")

    async def remove_token(self, jti: UUID) -> None:
        """Удаление токена по его JTI из всех связанных ключей."""
        token_data = await self.get_refresh_token_data(jti)
        if not token_data:
            logger.warning("Токен с jti %s не найден для удаления.", jti)
            return

        await self.redis.delete(f"refresh_token:{jti}")
        logger.info("Удалён токен с jti: %s", jti)

        user_id = token_data.user_id
        await self.redis.zrem(f"refresh_tokens:{user_id}", jti)
        logger.info("Токен с jti: %s удалён из списка refresh_tokens:%s", jti, user_id)

        fingerprint = token_data.fingerprint
        await self.redis.delete(f"refresh_token_index:{user_id}:{fingerprint}")
        logger.info(
            "Удалён индекс для user_id: %s и fingerprint: %s",
            user_id,
            fingerprint,
        )

    async def get_existing_jti(self, user_id: UUID, fingerprint: str) -> Optional[str]:
        """Получение существующего JTI для пользователя по fingerprint."""
        return await self.redis.get(  # type: ignore
            f"refresh_token_index:{user_id}:{fingerprint}"
        )
