import redis.asyncio as aioredis


class InvestmentService:
    def __init__(self, redis: aioredis.Redis):
        self.redis = redis

    async def get_investments(self):
        self.redis.get()
