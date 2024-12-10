from typing import AsyncIterable

import aiohttp
import redis.asyncio as aioredis
from dishka import Provider, provide, Scope, make_async_container
from gigachat import GigaChat

from bonds_gateway import BondsGateway
from currency_gateway import CurrenciesGateway
from gold_gateway import GoldGateway
from investments_service import InvestmentsService
from deposit_gateway import DepositGateway
from news.news_gateway import NewsGateway
from predict.config import GigaChatSettings
from redis_config import RedisConfig
from share_gateway import SharesGateway


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_config(self) -> GigaChatSettings:
        return GigaChatSettings.from_env()


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
        async with aiohttp.ClientSession() as session:
            yield session


class GatewayProvider(Provider):
    shares_gate = provide(SharesGateway, scope=Scope.REQUEST)
    bonds_gate = provide(BondsGateway, scope=Scope.REQUEST)
    currencies_gate = provide(CurrenciesGateway, scope=Scope.REQUEST)
    gold_gate = provide(GoldGateway, scope=Scope.REQUEST)
    deposit_gate = provide(DepositGateway, scope=Scope.REQUEST)
    news_gate = provide(NewsGateway, scope=Scope.REQUEST)
    giga_chat = provide(GigaChat, scope=Scope.REQUEST)


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=GigaChat)
    def provide_giga_chat(self, giga_chat_settings: GigaChatSettings) -> GigaChat:
        return GigaChat(
            credentials=giga_chat_settings.credentials,
            scope=giga_chat_settings.scope,
            model=giga_chat_settings.model,
        )
    investments_service = provide(InvestmentsService, scope=Scope.REQUEST)


container = make_async_container(
    SettingsProvider(), RedisProvider(), AsyncHTTPSession(), GatewayProvider(), ServiceProvider()
)
