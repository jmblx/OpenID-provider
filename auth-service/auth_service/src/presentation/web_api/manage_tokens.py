import logging
from fastapi.responses import ORJSONResponse
from application.common.auth_server_token_types import AuthServerTokens
from application.common.client_token_types import ClientTokens

logger = logging.getLogger(__name__)


base_refresh_token_settings = {
    "httponly": True,
    "secure": False,
    "max_age": 60 * 60 * 24 * 30,
    "expires": 60 * 60 * 24 * 30,
    "samesite": "lax",
}

base_access_token_settings = {
    "httponly": True,
    "secure": False,
    "max_age": 60 * 60 * 24 * 30,
    "expires": 60 * 60 * 24 * 30,
    "samesite": "strict",
}



def set_auth_server_tokens(response: ORJSONResponse, tokens: AuthServerTokens):
    response.set_cookie(**base_refresh_token_settings, key="refresh_token", value=tokens.get("refresh_token"))
    response.set_cookie(**base_access_token_settings, key="access_token", value=tokens.get("access_token"))


def change_active_account(response: ORJSONResponse, prev_account_id: str, prev_account_tokens: AuthServerTokens, new_tokens: AuthServerTokens):
    response.set_cookie(**base_refresh_token_settings,
        key=f"refresh_token:{prev_account_id}",
        value=prev_account_tokens.get("refresh_token")
    )
    response.set_cookie(**base_access_token_settings,
        key=f"access_token:{prev_account_id}",
        value=prev_account_tokens.get("access_token")
    )
    set_auth_server_tokens(response, new_tokens)


def set_client_tokens(response: ORJSONResponse, tokens: ClientTokens):
    response.set_cookie(**base_refresh_token_settings, key="client_refresh_token", value=tokens.get("refresh_token"))
    response.set_cookie(**base_access_token_settings, key="client_access_token", value=tokens.get("access_token"))
