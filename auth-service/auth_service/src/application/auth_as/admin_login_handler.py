import secrets
import uuid
from dataclasses import dataclass

from application.auth_as.common.admin_settings import AdminSettings
from application.common.interfaces.http_auth import HttpAdminSessionService, SessionID
from domain.exceptions.auth import InvalidAdminCredentialsError


@dataclass
class LoginAdminCommand:
    admin_username: str
    password: str


class LoginAdminOtherTokensHandler:
    def __init__(self, session_service: HttpAdminSessionService, admin_settings: AdminSettings):
        self.session_service = session_service
        self.admin_settings = admin_settings

    async def handle(self, command: LoginAdminCommand) -> SessionID:
        if not secrets.compare_digest(command.password, self.admin_settings.admin_password):
            raise InvalidAdminCredentialsError()
        session_id = await self.session_service.create_and_save_session(command.admin_username)
        return session_id
