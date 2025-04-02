import os

from dishka import Provider, Scope, provide

from application.auth_as.common.admin_settings import AdminSettings
from infrastructure.external_services.storage.config import MinIOConfig
from infrastructure.services.auth.config import JWTSettings


class SettingsProvider(Provider):
    storage_settings = provide(
        lambda *args: MinIOConfig(), scope=Scope.APP, provides=MinIOConfig
    )
    jwt_settings = provide(
        lambda *args: JWTSettings(), scope=Scope.APP, provides=JWTSettings
    )
    admin_settings = provide(
        lambda *args: AdminSettings(), scope=Scope.APP, provides=AdminSettings
    )
    # firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
