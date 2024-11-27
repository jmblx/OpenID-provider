from uuid import uuid4

import orjson
import redis.asyncio as aioredis
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from application.auth.commands.register_user_command import RegisterUserCommand
from application.client.interfaces.reader import ClientReader
from application.common.uow import Uow
from application.user.interfaces.reader import UserReader
from application.user.interfaces.repo import UserRepository
from domain.entities.auth.pkce import PKCEData
from domain.entities.client.value_objects import ClientID
from domain.entities.role.value_objects import RoleID
from domain.entities.user.model import User
from domain.entities.user.value_objects import HashedPassword, Email
from domain.exceptions.auth import (
    InvalidRedirectURLError,
    InvalidClientError,
    UserAlreadyExistsError,
)
from domain.services.security.pwd_service import HashService


class RegisterUserCommandHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        user_reader: UserReader,
        hash_service: HashService,
        redis_client: aioredis.Redis,
        client_reader: ClientReader,
        uow: Uow,
    ):
        self.user_repository = user_repository
        self.user_reader = user_reader
        self.hash_service = hash_service
        self.redis_client = redis_client
        self.client_reader = client_reader
        self.uow = uow

    async def handle(self, command: RegisterUserCommand) -> str:
        client_id_vo = ClientID(command.client_id)
        client = await self.client_reader.with_id(client_id_vo)
        if not client:
            raise InvalidClientError("Invalid client_id")

        if command.redirect_url not in client.allowed_redirect_urls:
            raise InvalidRedirectURLError("Invalid redirect URL")

        email_vo = Email(command.email)
        existing_user = await self.user_reader.get_by_email(email_vo)
        if existing_user:
            raise UserAlreadyExistsError("User already exists")

        hashed_password_vo = HashedPassword.create(
            command.password, self.hash_service
        )

        role_id_vo = RoleID(command.role_id)
        user = User(
            email=email_vo,
            hashed_password=hashed_password_vo,
            role_id=role_id_vo,
        )
        await self.user_repository.save(user)
        await self.uow.commit()
        auth_code = str(uuid4())

        pkce_data = PKCEData(
            code_challenge=command.code_challenge,
            code_challenge_method=command.code_challenge_method,
        )

        auth_code_data = {
            "user_email": user.email.value,
            "client_id": client_id_vo.value,
            "redirect_url": command.redirect_url,
            "code_challenge": pkce_data.code_challenge,
            "code_challenge_method": pkce_data.code_challenge_method,
        }

        temp_user_data = {
            "email": user.email.value,
            "hashed_password": user.hashed_password.value,
            "role_id": user.role_id.value,
        }

        await self.redis_client.set(
            f"auth_code:{auth_code}",
            orjson.dumps(auth_code_data),
            ex=600,
        )

        await self.redis_client.set(
            f"temp_user:{user.email.value}",
            orjson.dumps(temp_user_data),
            ex=600,
        )

        return auth_code
