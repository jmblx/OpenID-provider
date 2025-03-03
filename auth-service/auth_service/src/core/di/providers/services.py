from typing import Annotated

import argon2
from dishka import Provider, Scope, provide, FromComponent
from redis.asyncio import Redis

from application.auth_as.common.scopes_service import ScopesService
from application.common.interfaces.client_token_creation import ClientTokenCreationService
from application.common.interfaces.email_confirmation_service import (
    EmailConfirmationServiceI,
)
from application.common.interfaces.http_auth import HttpAuthServerService, HttpClientService
from application.common.interfaces.imedia_storage import StorageServiceInterface
from application.common.interfaces.jwt_service import JWTService
from application.common.interfaces.notify_service import NotifyService
from application.common.interfaces.auth_server_token_creation import AuthServerTokenCreationService
from application.common.interfaces.white_list import TokenWhiteListService
from application.common.services.auth_code import AuthorizationCodeStorage
from application.common.services.pkce import PKCEService
from application.common.services.client_service import ClientService
from application.common.id_provider import (
    IdentityProvider,
    HttpIdentityProvider,
)
from application.user.reset_pwd.service import ResetPwdService
from domain.common.services.pwd_service import PasswordHasher
from infrastructure.external_services.message_routing.notify_service import (
    NotifyServiceImpl,
)
from infrastructure.external_services.storage.minio_service import MinIOService

from infrastructure.services.auth.auth_code import (
    RedisAuthorizationCodeStorage,
)
from infrastructure.services.auth.client_auth_service import HttpClientServiceImpl
from infrastructure.services.auth.client_token_creation import ClientTokenCreationServiceImpl
from infrastructure.services.auth.jwt_service import JWTServiceImpl
from infrastructure.services.auth.reset_pwd_service import ResetPwdServiceImpl
from infrastructure.services.auth.scopes_service import ScopesServiceImpl
from infrastructure.services.auth.auth_server_token_creation import (
    AuthServerTokenCreationServiceImpl,
)
from infrastructure.services.auth.user_auth_server_service import (
    HttpAuthServerServiceImpl,
)
from infrastructure.services.auth.white_list_service import (
    AuthServerTokenService,
    ClientTokenService,
)
from infrastructure.services.security.pwd_service import PasswordHasherImpl
from infrastructure.services.user.email_confirmation_service import (
    EmailConfirmationService,
)
from infrastructure.services.user.user_service import UserServiceImpl


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
    jwt_service = provide(
        JWTServiceImpl, scope=Scope.REQUEST, provides=JWTService
    )
    http_auth_server_service = provide(
        HttpAuthServerServiceImpl,
        scope=Scope.REQUEST,
        provides=HttpAuthServerService,
    )
    token_creation_service = provide(
        AuthServerTokenCreationServiceImpl,
        scope=Scope.REQUEST,
        provides=AuthServerTokenCreationService,
    )
    client_token_creation_service = provide(ClientTokenCreationServiceImpl, scope=Scope.REQUEST, provides=ClientTokenCreationService)
    # token_white_list_service = provide(
    #     TokenWhiteListServiceImpl,
    #     scope=Scope.REQUEST,
    #     provides=TokenWhiteListService,
    # )
    client_service = provide(ClientService, scope=Scope.REQUEST)
    identity_provider = provide(
        HttpIdentityProvider, scope=Scope.REQUEST, provides=IdentityProvider
    )
    # investment_service = provide(InvestmentsService, scope=Scope.REQUEST)
    notify_service = provide(
        NotifyServiceImpl, scope=Scope.REQUEST, provides=NotifyService
    )
    email_confirmation_service = provide(
        EmailConfirmationService,
        scope=Scope.REQUEST,
        provides=EmailConfirmationServiceI,
    )
    reset_pwd_service = provide(
        ResetPwdServiceImpl, scope=Scope.REQUEST, provides=ResetPwdService
    )
    # user_service = provide(
    #     UserServiceImpl, scope=Scope.REQUEST, provides=UserService
    # )
    scopes_service = provide(
        ScopesServiceImpl, scope=Scope.REQUEST, provides=ScopesService
    )
    http_client_service = provide(HttpClientServiceImpl, scope=Scope.REQUEST, provides=HttpClientService)
    storage_service_interface = provide(MinIOService, scope=Scope.REQUEST, provides=StorageServiceInterface)

    # reg_validation_service = provide(
    #     RegUserValidationService,
    #     scope=Scope.REQUEST,
    #     provides=UserValidationService,
    # )


class AuthServerTokenProvider(Provider):
    """Провайдер для AuthServerTokenService."""

    component = "auth_server"

    @provide(scope=Scope.REQUEST)
    def provide_auth_server_service(
        self, redis: Annotated[Redis, FromComponent("")]
    ) -> TokenWhiteListService:
        return AuthServerTokenService(redis)


class ClientTokenProvider(Provider):
    """Провайдер для ClientTokenService."""

    component = "client"

    @provide(scope=Scope.REQUEST)
    def provide_client_service(
        self, redis: Annotated[Redis, FromComponent("")]
    ) -> TokenWhiteListService:
        return ClientTokenService(redis)
