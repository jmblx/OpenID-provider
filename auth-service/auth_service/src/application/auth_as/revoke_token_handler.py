from application.common.interfaces.http_auth import HttpAuthServerService
from application.common.auth_server_token_types import AuthServerRefreshToken


class RevokeTokenHandler:
    def __init__(self, auth_service: HttpAuthServerService):
        self.auth_service = auth_service

    async def handle(self, refresh_token: AuthServerRefreshToken) -> None:
        await self.auth_service.revoke(refresh_token)
