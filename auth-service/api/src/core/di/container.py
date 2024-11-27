from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from core.di.providers.db import DBProvider

# from core.di.providers.redis_provider import RedisProvider
from core.di.providers.repositories import RepositoriesProvider
from core.di.providers.services import ServiceProvider, ExternalAPIProvider
from core.di.providers.settings import SettingsProvider

# from core.di.providers.usecases import UseCaseProvider

container = make_async_container(
    DBProvider(),
    # RedisProvider(),
    RepositoriesProvider(),
    SettingsProvider(),
    # UseCaseProvider(),
    ServiceProvider(),
    ExternalAPIProvider(),
    FastapiProvider(),
)
