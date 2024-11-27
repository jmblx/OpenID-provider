from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from application.user.interfaces.reader import UserReader
from domain.entities.role.value_objects import RoleID
from domain.entities.user.model import User
from domain.entities.user.value_objects import Email, UserID, HashedPassword
from infrastructure.db.models.user_models import UserDB


class UserReaderImpl(UserReader):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_email(self, email: Email) -> Optional[User]:
        query = select(UserDB).where(UserDB.email == email.value)
        result = await self.db_session.execute(query)
        user_db = result.scalar_one_or_none()
        if not user_db:
            return None

        return self._convert_user_db_to_domain(user_db)

    async def get_by_id(self, user_id: UserID) -> Optional[User]:
        query = select(UserDB).where(UserDB.id == user_id.value)
        result = await self.db_session.execute(query)
        user_db = result.scalar_one_or_none()
        if not user_db:
            return None

        return self._convert_user_db_to_domain(user_db)

    def _convert_user_db_to_domain(self, user_db: UserDB) -> User:
        return User(
            id=UserID(user_db.id),
            email=Email(user_db.email),
            hashed_password=HashedPassword(user_db.hashed_password),
            role_id=RoleID(user_db.role_id),
            is_email_confirmed=user_db.is_email_confirmed,
        )
