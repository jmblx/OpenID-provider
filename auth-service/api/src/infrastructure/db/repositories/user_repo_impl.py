from operator import and_
from typing import cast
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.user.dto.user import UserCreateOutputDTO
from application.user.interfaces.repo import UserRepository, IdentificationFields
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email
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

    async def by_fields_with_clients(
        self, fields: IdentificationFields
    ) -> User | None:
        stmt = select(User).options(joinedload(User.clients))  # type: ignore

        filters = []
        for field, value in fields.items():
            if hasattr(User, field):
                column = getattr(User, field)
                filters.append(column == value)

        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def by_id(self, user_id: UserID) -> User | None:
        return await self.session.get(User, user_id)

    async def by_email(self, email: Email) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user
