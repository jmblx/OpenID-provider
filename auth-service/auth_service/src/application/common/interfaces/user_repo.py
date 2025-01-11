from abc import ABC, abstractmethod
from typing import TypedDict

from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email, HashedPassword


class IdentificationFields(TypedDict, total=False):
    id: UserID | None
    email: Email | None


class UserMutableFields(TypedDict, total=False):
    avatar_path: str
    hashed_password: HashedPassword


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        """Сохранить пользователя в базе данных."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user: User) -> None:
        """Удалить пользователя по ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_fields_with_clients(
        self, fields: IdentificationFields
    ) -> User | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UserID) -> User | None:
        """Получить пользователя по ID."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: Email) -> User | None:
        """Получить пользователя по email."""
        raise NotImplementedError

    # @abstractmethod
    # async def update_user_fields_by_id(self, user_id: UserID, upd_data: UserMutableFields):
    #     pass
