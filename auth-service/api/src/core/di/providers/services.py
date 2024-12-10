import argon2
from dishka import Provider, Scope, provide

from application.auth.interfaces.http_auth import HttpAuthService
from application.auth.interfaces.jwt_service import JWTService
from application.auth.interfaces.token_creation import TokenCreationService
from application.auth.interfaces.white_list import TokenWhiteListService
from application.auth.services.auth_code import AuthorizationCodeStorage
from application.auth.services.pkce import PKCEService
from application.client.service import ClientService
from application.common.id_provider import IdentityProvider, HttpIdentityProvider
from domain.common.services.pwd_service import PasswordHasher
from infrastructure.external_services.investments.service import InvestmentsService
# from domain.services.storage.storage_service import StorageServiceInterface
# from infrastructure.external_services.storage.minio_service import MinIOService
from infrastructure.services.auth.auth_code import (
    RedisAuthorizationCodeStorage,
)
from infrastructure.services.auth.http_auth_service import HttpAuthServiceImpl
from infrastructure.services.auth.jwt_service import JWTServiceImpl
from infrastructure.services.auth.token_creation_service import (
    TokenCreationServiceImpl,
)
from infrastructure.services.auth.white_list_service import (
    TokenWhiteListServiceImpl,
)
from infrastructure.services.security.pwd_service import PasswordHasherImpl


class ServiceProvider(Provider):

    # @provide(scope=Scope.REQUEST, provides=UserService)
    # def provide_user_service(
    #     self, user_repo: UserRepository
    # ) -> UserService:
    #     return UserServiceImpl(user_repo)
    # storage_service = provide(
    #     MinIOService, scope=Scope.REQUEST, provides=StorageServiceInterface
    # )
    ph = provide(
        lambda _: PasswordHasherImpl(argon2.PasswordHasher()),
        scope=Scope.REQUEST,
        provides=PasswordHasher,
    )
    pkce_service = provide(
        lambda _: PKCEService(), scope=Scope.APP, provides=PKCEService
    )
    auth_code_service = provide(
        RedisAuthorizationCodeStorage,
        scope=Scope.REQUEST,
        provides=AuthorizationCodeStorage,
    )
    jwt_service = provide(JWTServiceImpl, scope=Scope.REQUEST, provides=JWTService)
    http_auth_service = provide(
        HttpAuthServiceImpl, scope=Scope.REQUEST, provides=HttpAuthService
    )
    token_creation_service = provide(
        TokenCreationServiceImpl,
        scope=Scope.REQUEST,
        provides=TokenCreationService,
    )
    token_white_list_service = provide(
        TokenWhiteListServiceImpl,
        scope=Scope.REQUEST,
        provides=TokenWhiteListService,
    )
    client_service = provide(ClientService, scope=Scope.REQUEST)
    identity_provider = provide(HttpIdentityProvider, scope=Scope.REQUEST, provides=IdentityProvider)
    investment_service = provide(InvestmentsService, scope=Scope.REQUEST)
    # reg_validation_service = provide(
    #     RegUserValidationService,
    #     scope=Scope.REQUEST,
    #     provides=UserValidationService,
    # )
