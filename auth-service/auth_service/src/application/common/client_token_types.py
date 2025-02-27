from dataclasses import dataclass
from typing import NewType, TypedDict

from application.common.auth_server_token_types import BaseToken, RefreshTokenData, AuthServerAccessTokenPayload, \
    RefreshTokenPayload

ClientAccessToken = NewType("AccessToken", BaseToken)
ClientRefreshToken = NewType("RefreshToken", BaseToken)


@dataclass
class ClientRefreshTokenData(RefreshTokenData): ...

@dataclass
class ClientRefreshTokenWithData(ClientRefreshTokenData):
    token: ClientRefreshToken


class ClientAccessTokenPayload(AuthServerAccessTokenPayload):
    user_scopes: list[str]


class ClientRefreshTokenPayload(RefreshTokenPayload):
    client_id: int


class ClientTokens(TypedDict):
    access_token: ClientAccessToken
    refresh_token: ClientRefreshToken


