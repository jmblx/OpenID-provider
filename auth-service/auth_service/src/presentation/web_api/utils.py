import logging

from fastapi.responses import ORJSONResponse

from application.auth_as.common.types import AuthServerTokens


logger = logging.getLogger(__name__)


def render_auth_code_url(redirect_url: str, auth_code: str) -> str:
    if "{auth_code}" in redirect_url:
        return redirect_url.replace("{auth_code}", auth_code)
    return redirect_url + f"?auth_code={auth_code}"



def set_tokens(response: ORJSONResponse, tokens: AuthServerTokens, access_key: str, refresh_key: str):
    response.set_cookie(
        key=access_key,
        value=tokens.get("access_token"),
        httponly=True,
        secure=False,
        max_age=60 * 5,
        expires=60 * 5,
        samesite="lax",
    )
    response.set_cookie(
        key=refresh_key,
        value=tokens.get("refresh_token"),
        httponly=True,
        secure=False,
        max_age=60 * 60 * 24 * 30,
        expires=60 * 60 * 24 * 30,
        samesite="lax",
    )


def set_auth_server_tokens(response: ORJSONResponse, tokens: AuthServerTokens):
    set_tokens(response, tokens, "access_token", "refresh_token")


def set_client_tokens(response: ORJSONResponse, tokens: AuthServerTokens):
    set_tokens(response, tokens, "client_access_token", "client_refresh_token")
