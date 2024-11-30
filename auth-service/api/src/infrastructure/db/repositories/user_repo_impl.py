from typing import cast
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.user.dto.user import UserCreateOutputDTO
from application.user.interfaces.repo import UserRepository
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID
from infrastructure.db.exception_mapper import exception_mapper
from infrastructure.db.models.user_models import user_table


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @exception_mapper
    async def save(self, user: User) -> None:
        """
        Сохраняет пользователя в базе данных.
        """
        await self.session.merge(user)
        await self.session.flush()  # Обновляем id, если это новая запись

    async def delete(self, user_id: UserID) -> None:
        """
        Удаляет пользователя по его идентификатору.
        """
        query = select(user_table).where(user_table.c.id == user_id.value)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        if user:
            await self.session.delete(user)
