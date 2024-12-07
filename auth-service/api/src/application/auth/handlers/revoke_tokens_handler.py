from application.auth.interfaces.http_auth import HttpAuthService
from application.auth.token_types import RefreshToken


class RevokeTokensHandler:
    def __init__(self, auth_service: HttpAuthService):
        self.auth_service = auth_service

    async def handle(self, refresh_token: RefreshToken) -> None:
        await self.auth_service.revoke(refresh_token)
