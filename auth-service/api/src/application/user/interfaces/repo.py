from abc import ABC, abstractmethod

from application.user.dto.user import UserCreateOutputDTO
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> UserCreateOutputDTO:
        """Сохранить пользователя в базе данных."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: UserID) -> None:
        """Удалить пользователя по ID."""
        raise NotImplementedError
