from dishka import Provider, Scope, provide

from domain.services.storage.storage_service import StorageServiceInterface
from infrastructure.external_services.storage.minio_service import MinIOService
from infrastructure.services.auth.auth_code import (
    RedisAuthorizationCodeStorage,
)
from infrastructure.services.auth.http_auth_service import HttpAuthServiceImpl
from infrastructure.services.auth.jwt_service import JWTServiceImpl


class ServiceProvider(Provider):

    # @provide(scope=Scope.REQUEST, provides=UserService)
    # def provide_user_service(
    #     self, user_repo: UserRepository
    # ) -> UserService:
    #     return UserServiceImpl(user_repo)
    storage_service = provide(
        MinIOService, scope=Scope.REQUEST, provides=StorageServiceInterface
    )
    # reg_validation_service = provide(
    #     RegUserValidationService,
    #     scope=Scope.REQUEST,
    #     provides=UserValidationService,
    # )
