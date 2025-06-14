import logging

from fastapi.responses import ORJSONResponse
from fastapi import Request

from application.common.auth_server_token_types import AuthServerTokens
from application.common.client_token_types import ClientTokens
from domain.exceptions.auth import InvalidTokenError

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


def change_active_account(response: ORJSONResponse, prev_account_id: str, prev_account_tokens: AuthServerTokens, new_tokens: AuthServerTokens, new_active_account_id: str):
    response.set_cookie(**base_refresh_token_settings,
        key=f"refresh_token:{prev_account_id}",
        value=prev_account_tokens.get("refresh_token")
    )
    response.set_cookie(**base_access_token_settings,
        key=f"access_token:{prev_account_id}",
        value=prev_account_tokens.get("access_token")
    )
    response.delete_cookie(f"refresh_token:{new_active_account_id}")
    response.delete_cookie(f"access_token:{new_active_account_id}")
    set_auth_server_tokens(response, new_tokens)


def set_client_tokens(response: ORJSONResponse, tokens: ClientTokens):
    response.set_cookie(**base_refresh_token_settings, key="client_refresh_token", value=tokens.get("refresh_token"))
    response.set_cookie(**base_access_token_settings, key="client_access_token", value=tokens.get("access_token"))


def get_tokens_by_user_id(request: Request, user_id: str) -> AuthServerTokens:
    refresh_token = request.cookies.get(f"refresh_token:{user_id}")
    if not refresh_token:
        raise InvalidTokenError()
    access_token = request.cookies.get(f"access_token:{user_id}")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
