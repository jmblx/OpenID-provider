import logging
from dataclasses import dataclass

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
    redirect_url: str
    code_verifier: str
    code_challenge_method: PKCECodeChallengeMethod
    client_id: int
    scopes: dict[str, str] | None


class AuthenticateUserHandler:
    def __init__(
        self,
        auth_code_storage: AuthorizationCodeStorage,
        client_service: ClientService,
        user_repository: UserRepository,
        user_service: UserService,
        uow: Uow,
        pkce_service: PKCEService,
        password_hasher: PasswordHasher,
    ):
        self.user_repository = user_repository
        self.auth_code_storage = auth_code_storage
        self.client_service = client_service
        self.user_service = user_service
        self.uow = uow
        self.pkce_service = pkce_service
        self.password_hasher = password_hasher

    async def handle(self, command: AuthenticateUserCommand) -> str:
        client = await self.client_service.get_validated_client(
            ValidateClientRequest(
                client_id=command.client_id,
                redirect_url=command.redirect_url,
            )
        )
        if not client:
            logger.error(
                f"Client not found while adding client to user",
                extra={
                    "client_id": command.client_id,
                },
            )
            raise ClientNotFound()
        user: User | None = (
            await self.user_repository.get_by_fields_with_clients(
                {"email": Email(command.email)}
            )
        )
        if not user:
            raise UserNotFoundByEmailError(command.email)
        user.check_pwd(
            RawPassword(command.password), password_hasher=self.password_hasher
        )
        if client not in user.clients:
            await self.user_service.add_client_to_user(user, client)

        auth_code = self.auth_code_storage.generate_auth_code()
        pkce_data = PKCEData(
            code_verifier=command.code_verifier,
            code_challenge_method=command.code_challenge_method,
        )
        auth_code_data: AuthCodeData = {
            "user_id": str(user.id.value),
            "client_id": str(command.client_id),
            "redirect_url": command.redirect_url,
            "code_challenger": self.pkce_service.generate_code_challenge(
                pkce_data
            ),
        }

        await self.auth_code_storage.store_auth_code_data(
            auth_code, auth_code_data, expiration_time=6000
        )

        return auth_code
