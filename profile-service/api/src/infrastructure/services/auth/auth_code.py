import redis.asyncio as aioredis
import orjson
from typing import Optional
from application.auth.services.auth_code import (
    AuthorizationCodeStorage,
    AuthCodeData,
)


class RedisAuthorizationCodeStorage(AuthorizationCodeStorage):
    def __init__(self, redis_client: aioredis.Redis):
        self.redis_client = redis_client

    async def store_auth_code_data(
        self, auth_code: str, data: AuthCodeData, expiration_time: int = 600
    ) -> None:
        """
        Сохраняет данные авторизационного кода в Redis.
        """
        json_data = orjson.dumps(data)
        await self.redis_client.set(
            f"auth_code:{auth_code}", json_data, ex=expiration_time
        )

    async def retrieve_auth_code_data(self, auth_code: str) -> Optional[AuthCodeData]:
        """
        Извлекает данные, связанные с авторизационным кодом из Redis.
        """
        raw_data = await self.redis_client.get(f"auth_code:{auth_code}")
        if raw_data:
            return orjson.loads(raw_data)
        return None

    async def delete_auth_code_data(self, auth_code: str) -> None:
        """
        Удаляет данные, связанные с авторизационным кодом из Redis.
        """
        await self.redis_client.delete(f"auth_code:{auth_code}")
