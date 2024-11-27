from dishka import Provider, Scope, provide

from config import FirebaseConfig
from infrastructure.external_services.storage.config import MinIOConfig


class SettingsProvider(Provider):
    storage_settings = provide(
        lambda *args: MinIOConfig(), scope=Scope.APP, provides=MinIOConfig
    )
    # firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
