from abc import abstractmethod, ABC
from typing import Optional

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email


class UserReader(ABC):
    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        """Получить пользователя по email."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: UserID) -> Optional[User]:
        """Получить пользователя по ID."""
        raise NotImplementedError
