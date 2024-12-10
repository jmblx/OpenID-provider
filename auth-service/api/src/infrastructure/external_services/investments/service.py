import json

import redis.asyncio as aioredis


class InvestmentsService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def get_investments(self) -> dict[str, dict]:
        investments = await self.redis.get("data")
        return json.loads(investments)
