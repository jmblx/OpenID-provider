from dishka import provide, Provider, Scope

from application.auth.handlers.auth_user_handler import AuthenticateUserHandler
from application.auth.handlers.code_to_token_handler import CodeToTokenHandler
from application.client.handlers.register_client_hadler import (
    RegisterClientHandler,
)
from application.auth.handlers.register_user_handler import (
    RegisterUserHandler,
)
from application.role.handlers.create_role_handler import CreateRoleHandler


class HandlerProvider(Provider):
    reg_client_handler = provide(
        RegisterClientHandler,
        scope=Scope.REQUEST,
    )
    reg_user_handler = provide(
        RegisterUserHandler,
        scope=Scope.REQUEST,
    )
    code_to_token_handler = provide(
        CodeToTokenHandler, scope=Scope.REQUEST
    )
    login_handler = provide(AuthenticateUserHandler, scope=Scope.REQUEST)
    create_role_handler = provide(CreateRoleHandler, scope=Scope.REQUEST)
