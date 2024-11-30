from dishka import provide, Provider, Scope

from application.auth.handlers.auth_user_handler import AuthenticateUserCommandHandler
from application.auth.handlers.code_to_token_handler import CodeToTokenHandler
from application.auth.handlers.register_client_hadler import (
    RegisterClientHandler,
)
from application.auth.handlers.register_user_handler import (
    RegisterUserCommandHandler,
)


class HandlerProvider(Provider):
    reg_client_handler = provide(
        RegisterClientHandler,
        scope=Scope.REQUEST,
        provides=RegisterClientHandler,
    )
    reg_user_handler = provide(
        RegisterUserCommandHandler,
        scope=Scope.REQUEST,
        provides=RegisterUserCommandHandler,
    )
    code_to_token_handler = provide(
        CodeToTokenHandler, scope=Scope.REQUEST, provides=CodeToTokenHandler
    )
    login_handler = provide(AuthenticateUserCommandHandler, scope=Scope.REQUEST, provides=AuthenticateUserCommandHandler)
