from application.common.interfaces.http_auth import HttpAuthService
from application.common.token_types import (
    AccessToken,
    RefreshToken,
    Fingerprint,
)


class RefreshTokensHandler:
    def __init__(self, auth_service: HttpAuthService):
        self.auth_service = auth_service

    async def handle(
        self, refresh_token: RefreshToken, fingerprint: Fingerprint
    ) -> tuple[AccessToken, RefreshToken]:
        return await self.auth_service.refresh_tokens(
            refresh_token=refresh_token, fingerprint=fingerprint
        )
