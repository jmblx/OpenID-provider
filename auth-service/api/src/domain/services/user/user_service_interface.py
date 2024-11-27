from abc import abstractmethod, ABC
from uuid import UUID

from domain.entities.user.model import User
from domain.entities.user.value_objects import Email
from domain.services.entity_service import EntityService


class UserService(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: Email) -> User:
        pass
