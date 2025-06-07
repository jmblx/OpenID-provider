import os

from dishka import Provider, Scope, provide

from application.auth_as.common.admin_settings import AdminSettings
from infrastructure.external_services.storage.config import MinIOConfig
from infrastructure.services.auth.config import JWTSettings


class SettingsProvider(Provider):
    @staticmethod
    @provide(scope=Scope.APP)
    def provide_storage_settings() -> MinIOConfig:
        return MinIOConfig()

    @staticmethod
    @provide(scope=Scope.APP, provides=JWTSettings)
    def provide_jwt_settings() -> JWTSettings:
        return JWTSettings()

    @staticmethod
    @provide(scope=Scope.APP)
    def provide_admin_settings() -> AdminSettings:
        return AdminSettings()
    # firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
