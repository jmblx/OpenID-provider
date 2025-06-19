from dishka import Provider, Scope, provide

from application.auth_as.common.admin_settings import AdminSettings
from infrastructure.external_services.storage.config import MinIOConfig
from infrastructure.services.auth.config import JWTSettings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_storage_settings(self) -> MinIOConfig:
        return MinIOConfig()

    @provide(scope=Scope.APP, provides=JWTSettings)
    def provide_jwt_settings(self) -> JWTSettings:
        return JWTSettings()

    @provide(scope=Scope.APP)
    def provide_admin_settings(self) -> AdminSettings:
        return AdminSettings()

    # firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
