from typing import Optional, Any

from mypy.build import TypedDict
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from application.user.interfaces.reader import UserReader, IdentificationFields
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, UserID, HashedPassword


class UserReaderImpl(UserReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def with_email(self, email: Email) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def read_by_id(self, user_id: UserID) -> Optional[User]:
        return await self.session.get(User, user_id)

    async def read_by_fields_with_client(self, fields: IdentificationFields) -> Optional[User]:
        stmt = select(User).options(joinedload(User.clients)) # type: ignore

        filters = []
        for field, value in fields.items():
            if hasattr(User, field):
                column = getattr(User, field)
                filters.append(column == value)

        if filters:
            stmt = stmt.where(and_(*filters))

        result = await self.session.execute(stmt)
        return result.scalars().first()
