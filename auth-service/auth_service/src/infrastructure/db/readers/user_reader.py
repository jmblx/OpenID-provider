from sqlalchemy import text, select

from application.common.interfaces.user_reader import (
    UserReader, UserCardData,
)

from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email
from uuid import UUID

from infrastructure.db.models import user_table


class UserReaderImpl(UserReader):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_card_data_by_id(
        self, user_ids: list[UserID]
    ) -> dict[UUID, UserCardData]:
        query = select(User.id, User.email).where(user_table.c.id.in_(user_ids))
        user_card_data = (await self.session.execute(query)).all()
        return {user.id.value: {"email": user.email.value} for user in user_card_data}

