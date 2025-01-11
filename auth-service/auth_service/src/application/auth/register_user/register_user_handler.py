import secrets
from dataclasses import dataclass, field

from application.client.get_client.client_queries import ValidateClientRequest
from application.common.interfaces.email_confirmation_service import (
    EmailConfirmationServiceI,
    UserRegisterNotifyData,
)
from application.common.interfaces.notify_service import NotifyService
from application.common.services.auth_code import (
    AuthorizationCodeStorage,
    AuthCodeData,
)
from application.common.services.pkce import (
    PKCEData,
    PKCEService,
    PKCECodeChallengeMethod,
)
from application.common.services.client_service import ClientService
from application.common.uow import Uow
from application.common.interfaces.user_repo import UserRepository
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email
from domain.exceptions.user import UserAlreadyExistsError
from domain.common.services.pwd_service import PasswordHasher


@dataclass
class RegisterUserCommand:
    email: str
    password: str
    redirect_url: str
    client_id: int
    code_verifier: str
    code_challenge_method: PKCECodeChallengeMethod
    scopes: dict[str, str] | None
    role_id: int = field(default=1)


class RegisterUserHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        hash_service: PasswordHasher,
        auth_code_storage: AuthorizationCodeStorage,
        client_service: ClientService,
        uow: Uow,
        pkce_service: PKCEService,
        email_confirmation_service: EmailConfirmationServiceI,
    ):
        self.user_repository = user_repository
        self.hash_service = hash_service
        self.auth_code_storage = auth_code_storage
        self.client_service = client_service
        self.uow = uow
        self.pkce_service = pkce_service
        self.email_confirmation_service = email_confirmation_service

    async def handle(self, command: RegisterUserCommand) -> str:
        client = await self.client_service.get_validated_client(
            ValidateClientRequest(
                client_id=command.client_id,
                redirect_url=command.redirect_url,
            )
        )
        existing_user = await self.user_repository.get_by_email(
            Email(command.email)
        )
        if existing_user:
            raise UserAlreadyExistsError(existing_user.email.value)

        user_id = User.generate_id()
        user = User.create(
            user_id=user_id,
            role_id=command.role_id,
            email=command.email,
            raw_password=command.password,
            password_hasher=self.hash_service,
        )
        user.clients.append(client)
        await self.user_repository.save(user)

        auth_code = self.auth_code_storage.generate_auth_code()
        pkce_data = PKCEData(
            code_verifier=command.code_verifier,
            code_challenge_method=command.code_challenge_method,
        )
        email_confirmation_token = secrets.token_urlsafe(32)
        auth_code_data: AuthCodeData = {
            "user_id": str(user_id),
            "client_id": str(client.id.value),
            "redirect_url": command.redirect_url,
            "code_challenger": self.pkce_service.generate_code_challenge(
                pkce_data
            ),
        }
        await self.auth_code_storage.store_auth_code_data(
            auth_code, auth_code_data, expiration_time=6000
        )
        await self.uow.commit()

        await self.email_confirmation_service.save_confirmation_token(
            email_confirmation_token, user_id
        )
        notify_data: UserRegisterNotifyData = {
            "email_confirmation_token": email_confirmation_token,
            "email": command.email,
        }
        await self.email_confirmation_service.email_register_notify(
            notify_data
        )

        return auth_code
