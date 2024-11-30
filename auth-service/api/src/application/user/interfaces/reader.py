from abc import abstractmethod, ABC
from typing import Optional, TypedDict

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email


class IdentificationFields(TypedDict, total=False):
    id: UserID | None
    email: Email | None


class UserReader(ABC):
    @abstractmethod
    async def with_email(self, email: Email) -> Optional[User]:
        """Получить пользователя по email."""
        raise NotImplementedError

    @abstractmethod
    async def read_by_id(self, user_id: UserID) -> Optional[User]:
        """Получить пользователя по ID."""
        raise NotImplementedError

    @abstractmethod
    async def read_by_fields_with_client(self, fields: IdentificationFields) -> Optional[User]:
        raise NotImplementedError


