from abc import ABC, abstractmethod
from typing import TypedDict

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email


class IdentificationFields(TypedDict, total=False):
    id: UserID | None
    email: Email | None


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        """Сохранить пользователя в базе данных."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UserID) -> None:
        """Удалить пользователя по ID."""
        raise NotImplementedError

    @abstractmethod
    async def by_fields_with_clients(
        self, fields: IdentificationFields
    ) -> User | None: ...

    @abstractmethod
    async def by_id(self, user_id: UserID) -> User | None:
        """Получить пользователя по ID."""
        raise NotImplementedError

    @abstractmethod
    async def by_email(self, email: Email) -> User | None:
        """Получить пользователя по email."""
        raise NotImplementedError
