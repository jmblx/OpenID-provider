from typing import AsyncIterable

import aiohttp
import redis.asyncio as aioredis
from dishka import Provider, provide, Scope, make_async_container

from bonds_gateway import BondsGateway
from currency_gateway import CurrenciesGateway
from gold_gateway import GoldGateway
from investments_service import InvestmentsService
from redis_config import RedisConfig
from share_gateway import SharesGateway


class RedisProvider(Provider):
    @provide(scope=Scope.APP, provides=RedisConfig)
    def provide_redis_config(self) -> RedisConfig:
        return RedisConfig.from_env()

    @provide(scope=Scope.REQUEST, provides=aioredis.Redis)
    async def provide_redis(self, config: RedisConfig) -> AsyncIterable[aioredis.Redis]:
        redis = await aioredis.from_url(
            config.rd_uri, encoding="utf8", decode_responses=True
        )
        try:
            yield redis
        finally:
            await redis.close()


class AsyncHTTPSession(Provider):
    @provide(scope=Scope.REQUEST, provides=aiohttp.ClientSession)
    async def provide_session(self) -> AsyncIterable[aiohttp.ClientSession]:
        async with aiohttp.ClientSession as session:
            yield session


class GatewayProvider(Provider):
    shares_gate = provide(SharesGateway, scope=Scope.REQUEST)
    bonds_gate = provide(BondsGateway, scope=Scope.REQUEST)
    currencies_gate = provide(CurrenciesGateway, scope=Scope.REQUEST)
    gold_gate = provide(GoldGateway, scope=Scope.REQUEST)


class ServiceProvider(Provider):
    investments_service = provide(InvestmentsService, scope=Scope.REQUEST)

container = make_async_container(RedisProvider(), AsyncHTTPSession(), GatewayProvider(), ServiceProvider())
