from dishka import Provider, provide, Scope
from fastapi import Request

from application.common.token_types import (
    Fingerprint,
    RefreshToken,
    AccessToken,
)


class PresentationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=Fingerprint)
    async def provide_session(self, request: Request) -> Fingerprint:
        return Fingerprint(request.headers.get("fingerprint"))  # type: ignore

    @provide(scope=Scope.REQUEST, provides=RefreshToken)
    async def provide_session_from_cookie(
        self, request: Request
    ) -> RefreshToken:
        return RefreshToken(request.cookies.get("refresh_token"))

    @provide(scope=Scope.REQUEST, provides=AccessToken)
    async def provide_session_from_token(
        self, request: Request
    ) -> AccessToken:
        return AccessToken(request.cookies.get("access_token"))
