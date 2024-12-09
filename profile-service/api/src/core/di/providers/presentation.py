from dishka import Provider, provide, Scope
from fastapi import Request



# class PresentationProvider(Provider):
#     @provide(scope=Scope.REQUEST, provides=Fingerprint)
#     async def provide_session(self, request: Request) -> Fingerprint:
#         return Fingerprint(request.headers.get("fingerprint"))  # type: ignore
