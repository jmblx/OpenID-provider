from application.auth.commands.code_to_token_command import CodeToTokenCommand
from application.auth.services.pkce import PKCEData
from application.auth.token_types import AccessToken, RefreshToken, Fingerprint
from application.auth.interfaces.http_auth import HttpAuthService


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
