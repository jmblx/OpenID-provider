import secrets
from dataclasses import dataclass
from typing import cast
from uuid import UUID

from application.common.auth_server_token_types import (
    AuthServerTokens,
)
from application.common.interfaces.email_confirmation_service import (
    EmailConfirmationServiceI,
    UserRegisterNotifyData,
)
from application.common.interfaces.http_auth import HttpAuthServerService
from application.common.interfaces.user_repo import UserRepository
from application.common.uow import Uow
from domain.common.services.pwd_service import PasswordHasher
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email
from domain.exceptions.user import UserAlreadyExistsError


@dataclass
class RegisterUserCommand:
    email: str
    password: str


class RegisterUserResult(AuthServerTokens):
    user_id: UUID


class RegisterUserHandler:
    def __init__(
        self,
        user_repo: UserRepository,
        hash_service: PasswordHasher,
        uow: Uow,
        email_confirmation_service: EmailConfirmationServiceI,
        auth_server_service: HttpAuthServerService,
    ):
        self.user_repository = user_repo
        self.hash_service = hash_service
        self.uow = uow
        self.email_confirmation_service = email_confirmation_service
        self.auth_server_service = auth_server_service

    async def handle(self, command: RegisterUserCommand) -> RegisterUserResult:
        existing_user = await self.user_repository.get_by_email(
            Email(command.email)
        )
        if existing_user:
            raise UserAlreadyExistsError(existing_user.email.value)

        user_id = User.generate_id()
        user = User.create(
            user_id=user_id,
            email=command.email,
            raw_password=command.password,
            password_hasher=self.hash_service,
        )
        await self.user_repository.save(user)
        auth_tokens = await self.auth_server_service.create_and_save_tokens(
            user
        )
        email_confirmation_token = secrets.token_urlsafe(32)
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

        await self.uow.commit()
        result = {**auth_tokens, "user_id": user_id}
        return cast(RegisterUserResult, result)
