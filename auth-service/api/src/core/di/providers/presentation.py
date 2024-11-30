from dishka import Provider, provide, Scope
from fastapi import Request

from application.auth.token_types import Fingerprint


class PresentationProvider(Provider):
    @provide(scope=Scope.REQUEST, provides=Fingerprint)
    async def provide_session(self, request: Request) -> Fingerprint:
        return Fingerprint(request.headers.get("fingerprint"))  # type: ignore
