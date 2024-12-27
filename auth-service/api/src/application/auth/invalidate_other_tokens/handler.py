from dataclasses import dataclass

from application.common.interfaces.http_auth import HttpAuthService
from application.common.token_types import RefreshToken, Fingerprint


@dataclass
class InvalidateOtherTokensCommand:
    fingerprint: Fingerprint
    refresh_token: RefreshToken


class InvalidateOtherTokensHandler:
    def __init__(self, http_auth_service: HttpAuthService):
        self.http_auth_service = http_auth_service

    async def handle(self, command: InvalidateOtherTokensCommand) -> None:
        await self.http_auth_service.invalidate_other_tokens(command.refresh_token, command.fingerprint)
