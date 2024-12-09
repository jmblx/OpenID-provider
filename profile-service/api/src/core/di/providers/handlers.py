from dishka import provide, Provider, Scope

from application.auth.handlers.auth_user_handler import AuthenticateUserHandler
from application.auth.handlers.code_to_token_handler import CodeToTokenHandler
from application.auth.handlers.refresh_tokens_handler import RefreshTokensHandler
from application.auth.handlers.revoke_tokens_handler import RevokeTokensHandler
from application.client.handlers.register_client_hadler import (
    RegisterClientHandler,
)
from application.auth.handlers.register_user_handler import (
    RegisterUserHandler,
)
from application.client.queries.client_queries import ClientAuthValidationQueryHandler
from application.role.handlers.create_role_handler import CreateRoleHandler


class HandlerProvider(Provider):
    ...
