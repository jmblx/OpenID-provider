import logging
from dataclasses import dataclass

from application.auth_as.common.types import AuthServerTokens
from application.common.interfaces.http_auth import HttpAuthServerService
from application.common.services.auth_code import (
    AuthorizationCodeStorage,
    AuthCodeData,
)
from application.common.services.pkce import (
    PKCEData,
    PKCEService,
    PKCECodeChallengeMethod,
)
from application.client.client_queries import ValidateClientRequest
from application.common.services.client_service import ClientService
from application.common.auth_server_token_types import RefreshToken, AccessToken
from application.common.uow import Uow
from application.common.interfaces.user_repo import UserRepository
from application.user.common.user_service import UserService
from domain.common.services.pwd_service import PasswordHasher
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, RawPassword
from domain.exceptions.client import ClientNotFound
from domain.exceptions.user import UserNotFoundByEmailError


logger = logging.getLogger(__name__)


@dataclass
class AuthenticateUserCommand:
    email: str
    password: str


class AuthenticateUserHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        auth_server_service: HttpAuthServerService,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.auth_server_service = auth_server_service

    async def handle(
        self, command: AuthenticateUserCommand
    ) -> AuthServerTokens:
        user: User | None = await self.user_repository.get_by_email(Email(command.email))

        if not user:
            raise UserNotFoundByEmailError(command.email)
        user.check_pwd(
            RawPassword(command.password), password_hasher=self.password_hasher
        )
        tokens = await self.auth_server_service.create_and_save_tokens(user)
        return tokens
