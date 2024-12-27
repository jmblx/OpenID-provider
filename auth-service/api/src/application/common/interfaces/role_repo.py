from abc import ABC, abstractmethod

from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleID


class RoleRepository(ABC):
    @abstractmethod
    async def save(self, role: Role) -> RoleID:
        pass
