from dishka import provide, Provider, Scope

from application.auth.handlers.auth_user_handler import AuthenticateUserHandler
from application.auth.handlers.code_to_token_handler import CodeToTokenHandler
from application.auth.handlers.refresh_tokens_handler import RefreshTokensHandler
from application.auth.handlers.revoke_tokens_handler import RevokeTokensHandler
from application.client.handlers.add_allowed_url import AddAllowedRedirectUrlCommandHandler
from application.client.handlers.register_client_hadler import (
    RegisterClientHandler,
)
from application.auth.handlers.register_user_handler import (
    RegisterUserHandler,
)
from application.client.handlers.rename_client import RenameClientCommandHandler
from application.client.queries.client_queries import ClientAuthValidationQueryHandler
from application.investments.queries import InvestmentsQueryHandler
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
    code_to_token_handler = provide(CodeToTokenHandler, scope=Scope.REQUEST)
    login_handler = provide(AuthenticateUserHandler, scope=Scope.REQUEST)
    create_role_handler = provide(CreateRoleHandler, scope=Scope.REQUEST)
    revoke_tokens_handler = provide(RevokeTokensHandler, scope=Scope.REQUEST)
    refresh_tokens_handler = provide(RefreshTokensHandler, scope=Scope.REQUEST)
    client_auth_validation_query_handler = provide(ClientAuthValidationQueryHandler, scope=Scope.REQUEST)
    rename_client_command_handler = provide(RenameClientCommandHandler, scope=Scope.REQUEST)
    add_allowed_redirect_url_command_handler = provide(AddAllowedRedirectUrlCommandHandler, scope=Scope.REQUEST)
    get_investments_query_handler = provide(InvestmentsQueryHandler, scope=Scope.REQUEST)
