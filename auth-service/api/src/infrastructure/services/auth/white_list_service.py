import logging
from dataclasses import asdict
from typing import Optional, Any
from uuid import UUID

import orjson
from redis.asyncio import Redis
from application.auth.interfaces.white_list import TokenWhiteListService
from application.auth.token_types import RefreshTokenData
from domain.entities.user.value_objects import UserID

logger = logging.getLogger(__name__)


class TokenWhiteListServiceImpl(TokenWhiteListService):
    """Реализация сервиса управления белым списком токенов с использованием Redis."""

    def __init__(self, redis: Redis):
        self.redis = redis

    def _serialize_refresh_token_data(
        self, refresh_token_data: RefreshTokenData
    ) -> dict:
        """Приводит все поля к типам, которые можно сериализовать в JSON (UUID -> str)."""
        return {
            "jti": str(refresh_token_data.jti),
            "user_id": str(refresh_token_data.user_id.value),
            "fingerprint": refresh_token_data.fingerprint,
            "created_at": refresh_token_data.created_at.isoformat(),
        }

    async def save_refresh_token(
        self, refresh_token_data: RefreshTokenData
    ) -> None:
        jti = refresh_token_data.jti
        user_id = refresh_token_data.user_id
        fingerprint = refresh_token_data.fingerprint
        created_at = refresh_token_data.created_at.timestamp()

        existing_jti = await self.get_existing_jti(user_id, fingerprint)
        if existing_jti:
            logger.info("Найден существующий токен с jti: %s", existing_jti)
            await self.redis.delete(f"refresh_token:{existing_jti}")
            await self.redis.zrem(f"refresh_tokens:{user_id}", existing_jti)
        else:
            logger.info(
                "Не найден существующий токен для user_id: %s и fingerprint: %s",
                user_id,
                fingerprint,
            )

        serialized_token_data = self._serialize_refresh_token_data(
            refresh_token_data
        )

        await self.redis.hset(
            f"refresh_token:{jti}", mapping=serialized_token_data
        )
        await self.redis.set(
            f"refresh_token_index:{user_id.value}:{fingerprint}", jti
        )
        logger.info("Сохранён новый токен с jti: %s", jti)

        await self.redis.zadd(
            f"refresh_tokens:{user_id.value}", {jti: created_at}
        )

    async def get_refresh_token_data(
        self, jti: UUID
    ) -> Optional[RefreshTokenData]:
        token_data = await self.redis.hgetall(f"refresh_token:{jti}")
        if not token_data:
            return None
        return RefreshTokenData(**token_data)

    async def remove_old_tokens(
        self, user_id: UserID, fingerprint: str, limit: int
    ) -> None:
        num_tokens = await self.redis.zcard(f"refresh_tokens:{user_id}")
        if num_tokens > limit:
            oldest_jti_list = await self.redis.zrange(
                f"refresh_tokens:{user_id}", 0, 0
            )
            if oldest_jti_list:
                oldest_jti = oldest_jti_list[0]
                logger.info(
                    "Удаление самого старого токена с jti: %s", oldest_jti
                )
                await self.redis.zrem(f"refresh_tokens:{user_id}", oldest_jti)
                await self.redis.delete(f"refresh_token:{oldest_jti}")
                await self.redis.delete(
                    f"refresh_token_index:{user_id}:{fingerprint}"
                )

    async def remove_token(self, jti: UUID) -> None:
        """Удаление токена по его JTI."""
        await self.redis.delete(f"refresh_token:{jti}")
        logger.info("Удалён токен с jti: %s", jti)

    async def get_existing_jti(
        self, user_id: UserID, fingerprint: str
    ) -> Optional[str]:
        """Получение существующего JTI для пользователя по fingerprint."""
        return await self.redis.get(
            f"refresh_token_index:{user_id.value}:{fingerprint}"
        )
