from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import sqlalchemy.dialects.postgresql as sa_pg
from sqlalchemy.orm import joinedload

from application.common.interfaces.user_repo import (
    UserRepository,
    IdentificationFields,
)
from domain.entities.role.model import Role
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email
from infrastructure.db.exception_mapper import exception_mapper
from infrastructure.db.models.secondary import user_role_association


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

    async def add_roles_to_user(
        self, user_id: UserID, role_ids: list[int]
    ) -> None:
        if not role_ids:
            return

        values = [
            {"user_id": user_id.value, "role_id": role_id}
            for role_id in role_ids
        ]

        stmt = (
            sa_pg.insert(user_role_association)
            .values(values)
            .on_conflict_do_nothing()
        )

        await self.session.execute(stmt)
        await self.session.commit()
