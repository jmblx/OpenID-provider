import argon2
from dishka import Provider, Scope, provide

from application.auth.scopes_service import ScopesService
from application.common.interfaces.email_confirmation_service import (
    EmailConfirmationServiceI,
)
from application.common.interfaces.http_auth import HttpAuthService
from application.common.interfaces.jwt_service import JWTService
from application.common.interfaces.notify_service import NotifyService
from application.common.interfaces.token_creation import TokenCreationService
from application.common.interfaces.white_list import TokenWhiteListService
from application.common.services.auth_code import AuthorizationCodeStorage
from application.common.services.pkce import PKCEService
from application.common.services.client_service import ClientService
from application.common.id_provider import (
    IdentityProvider,
    HttpIdentityProvider,
)
from application.user.reset_pwd.service import ResetPwdService
from application.user.user_service import UserService
from domain.common.services.pwd_service import PasswordHasher
from infrastructure.external_services.message_routing.notify_service import (
    NotifyServiceImpl,
)

from infrastructure.services.auth.auth_code import (
    RedisAuthorizationCodeStorage,
)
from infrastructure.services.auth.http_auth_service import HttpAuthServiceImpl
from infrastructure.services.auth.jwt_service import JWTServiceImpl
from infrastructure.services.auth.reset_pwd_service import ResetPwdServiceImpl
from infrastructure.services.auth.scopes_service import ScopesServiceImpl
from infrastructure.services.auth.token_creation_service import (
    TokenCreationServiceImpl,
)
from infrastructure.services.auth.white_list_service import (
    TokenWhiteListServiceImpl,
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
    identity_provider = provide(
        HttpIdentityProvider, scope=Scope.REQUEST, provides=IdentityProvider
    )
    # investment_service = provide(InvestmentsService, scope=Scope.REQUEST)
    notify_service = provide(
        NotifyServiceImpl, scope=Scope.REQUEST, provides=NotifyService
    )
    user_service = provide(
        UserServiceImpl, scope=Scope.REQUEST, provides=UserService
    )
    # reg_validation_service = provide(
    #     RegUserValidationService,
    #     scope=Scope.REQUEST,
    #     provides=UserValidationService,
    # )
