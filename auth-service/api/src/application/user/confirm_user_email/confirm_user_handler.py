from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from application.common.interfaces.user_repo import UserRepository
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email


@dataclass
class ConfirmUserCommand:
    confirmation_code: str


class ConfirmUserCommandHandler:
    def __init__(self, user_repository: UserRepository, redis_client: aioredis.Redis):
        self.user_repository = user_repository
        self.redis_client = redis_client

    async def handle(self, command: ConfirmUserCommand, session: AsyncSession) -> User:
        email = await self.redis_client.get(f"confirm:{command.confirmation_code}")
        if not email:
            raise Exception("Неверный или истекший код подтверждения")

        email_vo = Email(email.decode())

        user_data = await self.redis_client.get(f"temp_user:{email_vo.value}")
        if not user_data:
            raise Exception("Пользователь не найден в временном хранилище")

        user = ...

        user.confirm_email()

        await self.user_repository.save(user)

        await session.commit()

        # Удаляем временные данные из Redis
        await self.redis_client.delete(f"confirm:{command.confirmation_code}")
        await self.redis_client.delete(f"temp_user:{email_vo.value}")

        return user
