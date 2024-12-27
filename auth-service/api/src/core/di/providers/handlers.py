from dishka import provide, Provider, Scope

from application.auth.code_to_token.code_to_token_handler import CodeToTokenHandler
from application.auth.invalidate_other_tokens.handler import InvalidateOtherTokensHandler
from application.auth.login_user.auth_user_handler import AuthenticateUserHandler
from application.auth.refresh_tokens.refresh_tokens_handler import RefreshTokensHandler
from application.auth.register_user.register_user_handler import RegisterUserHandler
from application.auth.revoke_token.revoke_token_handler import RevokeTokenHandler
from application.client.add_allowed_redirect_url.add_allowed_url import AddAllowedRedirectUrlCommandHandler
from application.client.get_client.client_queries import ClientAuthValidationQueryHandler
from application.client.register_client.register_client_hadler import (
    RegisterClientHandler,
)
from application.client.rename_client.rename_client import RenameClientCommandHandler
from application.investments.read_all_investments.read_all_investments_handler import InvestmentsQueryHandler
from application.strategy.read_strategy.strategy_query_handler import StrategyQueryHandler
from application.user.buy_investments.buy_investment_handler import BuyInvestmentHandler
from application.user.sell_investments.sell_investment_handler import SellInvestmentHandler
from application.create_role.create_role_handler import CreateRoleHandler
from application.strategy.create_new_strategy.create_new_hanlder import CreateNewStrategyHanlder
from application.get_user_notifications.notification_query_handler import NotificationQueryHandler


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
    revoke_tokens_handler = provide(RevokeTokenHandler, scope=Scope.REQUEST)
    refresh_tokens_handler = provide(RefreshTokensHandler, scope=Scope.REQUEST)
    client_auth_validation_query_handler = provide(
        ClientAuthValidationQueryHandler, scope=Scope.REQUEST
    )
    rename_client_command_handler = provide(
        RenameClientCommandHandler, scope=Scope.REQUEST
    )
    add_allowed_redirect_url_command_handler = provide(
        AddAllowedRedirectUrlCommandHandler, scope=Scope.REQUEST
    )
    get_investments_query_handler = provide(
        InvestmentsQueryHandler, scope=Scope.REQUEST
    )
    create_new_strategy_hanlder = provide(CreateNewStrategyHanlder, scope=Scope.REQUEST)
    read_strategy_hanlder = provide(StrategyQueryHandler, scope=Scope.REQUEST)
    sell_investment_handler = provide(SellInvestmentHandler, scope=Scope.REQUEST)
    buy_investment_handler = provide(BuyInvestmentHandler, scope=Scope.REQUEST)
    notification_query_handler = provide(NotificationQueryHandler, scope=Scope.REQUEST)
    invalidate_tokens_exc_cur_handler = provide(InvalidateOtherTokensHandler, scope=Scope.REQUEST)
