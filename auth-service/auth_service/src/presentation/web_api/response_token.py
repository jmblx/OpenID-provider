import logging
from fastapi.responses import ORJSONResponse
from application.auth_as.common.types import AuthServerTokens
from application.common.client_token_types import ClientTokens

logger = logging.getLogger(__name__)


def set_tokens(response: ORJSONResponse, tokens: AuthServerTokens | ClientTokens, refresh_key: str, access_key):
    response.set_cookie(
        key=refresh_key,
        value=tokens.get("refresh_token"),
        httponly=True,
        secure=False,
        max_age=60 * 60 * 24 * 30,
        expires=60 * 60 * 24 * 30,
        samesite="lax",
        # samesite="none"
    )
    response.set_cookie(
        key=access_key,
        value=tokens.get("access_token"),
        httponly=True,
        secure=False,
        max_age=60 * 60 * 24 * 30,
        expires=60 * 60 * 24 * 30,
        samesite="strict",
    )


def set_auth_server_tokens(response: ORJSONResponse, tokens: AuthServerTokens):
    set_tokens(response, tokens, "refresh_token", "access_token")


def set_client_tokens(response: ORJSONResponse, tokens: ClientTokens):
    set_tokens(response, tokens, "client_refresh_token", "client_access_token")