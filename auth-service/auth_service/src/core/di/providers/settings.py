import os

from dishka import Provider, Scope, provide

from application.auth_as.common.admin_settings import AdminSettings
from infrastructure.external_services.storage.config import MinIOConfig
from infrastructure.services.auth.config import JWTSettings


class SettingsProvider(Provider):
    storage_settings = provide(
        MinIOConfig, scope=Scope.APP
    )

    @staticmethod
    @provide(scope=Scope.APP, provides=JWTSettings)
    def provide_jwt_settings() -> JWTSettings:
        return JWTSettings()

    admin_settings = provide(
        AdminSettings, scope=Scope.APP
    )
    # firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
