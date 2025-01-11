from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from application.common.interfaces.user_repo import (
    UserRepository,
    IdentificationFields,
    UserMutableFields,
)
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

    async def delete(self, user: User) -> None:
        """
        Удаляет пользователя по его идентификатору.
        """
        await self.session.delete(user)

    async def get_by_fields_with_clients(
        self, fields: IdentificationFields
    ) -> User | None:
        query = select(User).options(joinedload(User.clients))

        for field, value in fields.items():
            if hasattr(User, field):
                query = query.where(getattr(User, field) == value)

        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_id(self, user_id: UserID) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_email(self, email: Email) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    # async def update_user_fields_by_id(self, user_id: UserID, upd_data: UserMutableFields) ->:
    #     query = select(User).where(User.id == user_id)
    #     result = await self.session.execute(query)
    #     user = result.scalar_one_or_none()
    #     if user:
    #         for field, value in upd_data.items():
    #             if hasattr(user, field):
    #                 setattr(user, field, value)
