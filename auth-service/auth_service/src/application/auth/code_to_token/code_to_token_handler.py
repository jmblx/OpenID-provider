from dataclasses import dataclass

from application.common.token_types import (
    AccessToken,
    RefreshToken,
    Fingerprint,
)
from application.common.interfaces.http_auth import HttpAuthService


@dataclass
class CodeToTokenCommand:
    auth_code: str
    code_challenger: str
    redirect_url: str
    scopes: list[str]


class CodeToTokenHandler:
    def __init__(self, auth_service: HttpAuthService):
        self.auth_service = auth_service

    async def handle(
        self, command: CodeToTokenCommand, fingerprint: Fingerprint
    ) -> tuple[AccessToken, RefreshToken]:
        access_token, refresh_token = (
            await self.auth_service.authenticate_by_auth_code(
                command.auth_code,
                command.redirect_url,
                fingerprint,
                command.code_challenger,
            )
        )

        return access_token, refresh_token
