from sqlalchemy.ext.asyncio import AsyncSession

from application.user.interfaces.reader import UserReader


class UserReaderImpl(UserReader):
    def __init__(self, session: AsyncSession):
        self.session = session
