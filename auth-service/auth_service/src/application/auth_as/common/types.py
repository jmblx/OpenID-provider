from typing import TypedDict, NewType

from application.common.auth_server_token_types import BaseToken

AuthServerAccessToken = NewType("AuthServerAccessToken", BaseToken)
AuthServerRefreshToken = NewType("AuthServerRefreshToken", BaseToken)


class AuthServerTokens(TypedDict):
    access_token: AuthServerAccessToken
    refresh_token: AuthServerRefreshToken
