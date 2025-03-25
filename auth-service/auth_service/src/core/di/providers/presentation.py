from dishka import Provider, provide, Scope
from fastapi import Request

from application.common.auth_server_token_types import (
    Fingerprint,
    RefreshToken,
    AccessToken,
)
from application.common.client_token_types import ClientAccessToken, ClientRefreshToken


class PresentationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=Fingerprint)
    async def provide_session(self, request: Request) -> Fingerprint:
        return Fingerprint(request.headers.get("X-Device-Fingerprint"))  # type: ignore

    @provide(scope=Scope.REQUEST, provides=RefreshToken)
    async def provide_session_from_cookie(
        self, request: Request
    ) -> RefreshToken:
        return RefreshToken(request.cookies.get("refresh_token"))

    @provide(scope=Scope.REQUEST, provides=AccessToken)
    async def provide_session_from_token(
        self, request: Request
    ) -> AccessToken:
        return AccessToken(request.headers.get("Authorization").replace("Bearer ", ""))

    @provide(scope=Scope.REQUEST, provides=ClientAccessToken)
    async def provide_client_access_token(
        self, request: Request
    ) -> ClientAccessToken:
        return ClientAccessToken(request.headers.get("Authorization").replace("Bearer ", ""))

    @provide(scope=Scope.REQUEST, provides=ClientRefreshToken)
    async def provide_client_refresh_token(
        self, request: Request
    ) -> ClientRefreshToken:
        return ClientRefreshToken(request.cookies.get("client_refresh_token"))
