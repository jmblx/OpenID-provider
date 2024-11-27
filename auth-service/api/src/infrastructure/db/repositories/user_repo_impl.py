from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.user.dto.user import UserCreateOutputDTO
from application.user.interfaces.repo import UserRepository
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID
from infrastructure.db.models.user_models import UserDB, user_table


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> UserCreateOutputDTO:
        user_db = self._convert_domain_to_user_db(user)
        await self.session.merge(user_db)
        return UserCreateOutputDTO(user_id=user_db.id)

    async def delete(self, user_id: UserID) -> None:
        query = select(user_table).where(user_table.c.id == user_id.value)
        result = await self.session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db:
            await self.session.delete(user_db)

    def _convert_domain_to_user_db(self, user: User) -> UserDB:
        return UserDB(
            id=user.id.value,
            email=user.email.value,
            hashed_password=user.hashed_password.value,
            role_id=user.role_id.value,
            is_email_confirmed=user.is_email_confirmed,
        )
