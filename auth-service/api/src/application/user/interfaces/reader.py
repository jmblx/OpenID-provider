from abc import abstractmethod, ABC
from typing import Optional, TypedDict

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email


class IdentificationFields(TypedDict, total=False):
    id: UserID | None
    email: Email | None


class UserReader(ABC):
    @abstractmethod
    async def by_email(self, email: Email) -> User | None:
        """Получить пользователя по email."""
        raise NotImplementedError

    @abstractmethod
    async def by_id(self, user_id: UserID) -> User | None:
        """Получить пользователя по ID."""
        raise NotImplementedError

    @abstractmethod
    async def by_fields_with_clients(self, fields: IdentificationFields) -> User | None:
        raise NotImplementedError
