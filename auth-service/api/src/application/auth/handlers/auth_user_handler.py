from application.auth.commands.auth_user_command import AuthenticateUserCommand
from application.auth.services.token_service import TokenService
from application.user.interfaces.reader import UserReader
from domain.entities.user.value_objects import Email
from infrastructure.services.security.pwd_service import HashServiceImpl


class AuthenticateUserCommandHandler:
    def __init__(
        self,
        user_reader: UserReader,
        hash_service: HashServiceImpl,
        token_service: TokenService,
    ):
        self.user_reader = user_reader
        self.hash_service = hash_service
        self.token_service = token_service

    async def handle(self, command: AuthenticateUserCommand):
        email_vo = Email(command.email)
        user = await self.user_reader.get_by_email(email_vo)
        if not user:
            raise Exception("Неверные учетные данные")

        if not user.check_password(command.password, self.hash_service):
            raise Exception("Неверные учетные данные")

        if not user.is_email_confirmed:
            raise Exception("Email не подтвержден")

        access_token = self.token_service.create_access_token(user)
        refresh_token = self.token_service.create_refresh_token(user)
        await self.token_service.whitelist_token(access_token)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": self.token_service.jwt_settings.access_token_expire_minutes
            * 60,
            "scope": user.get_scopes(),
        }
