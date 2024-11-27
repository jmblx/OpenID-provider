import logging
from dataclasses import asdict
from datetime import datetime
from typing import Optional

from redis.asyncio import Redis

from application.auth.services.white_list import TokenWhiteListService
from application.auth.token_types import RefreshTokenData, JTI
from domain.entities.user.value_objects import UserID

logger = logging.getLogger(__name__)


class TokenWhiteListServiceImpl(TokenWhiteListService):
    """Реализация сервиса управления белым списком токенов с использованием Redis."""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_refresh_token(
        self, refresh_token_data: RefreshTokenData
    ) -> None:
        jti = refresh_token_data.jti
        user_id = refresh_token_data.user_id
        fingerprint = refresh_token_data.fingerprint
        created_at = datetime.fromisoformat(
            refresh_token_data.created_at
        ).timestamp()

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

        await self.redis.hset(
            f"refresh_token:{jti}", mapping=asdict(refresh_token_data)
        )
        await self.redis.set(
            f"refresh_token_index:{user_id}:{fingerprint}", jti
        )
        logger.info("Сохранён новый токен с jti: %s", jti)

        await self.redis.zadd(f"refresh_tokens:{user_id}", {jti: created_at})

    async def remove_oldest_token(
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

    async def get_refresh_token_data(
        self, jti: JTI
    ) -> Optional[RefreshTokenData]:
        token_data = await self.redis.hgetall(f"refresh_token:{jti}")
        if not token_data:
            return None
        return RefreshTokenData(**token_data)

    async def get_existing_jti(
        self, user_id: UserID, fingerprint: str
    ) -> Optional[str]:
        return await self.redis.get(
            f"refresh_token_index:{user_id}:{fingerprint}"
        )
