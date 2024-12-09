from dishka import Provider, Scope, provide

from infrastructure.external_services.storage.config import MinIOConfig
from infrastructure.services.auth.config import JWTSettings


class SettingsProvider(Provider):
    storage_settings = provide(
        lambda *args: MinIOConfig(), scope=Scope.APP, provides=MinIOConfig
    )
    jwt_settings = provide(
        lambda *args: JWTSettings(), scope=Scope.APP, provides=JWTSettings
    )
    # firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
