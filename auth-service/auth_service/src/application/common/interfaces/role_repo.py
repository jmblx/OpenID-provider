from abc import ABC, abstractmethod
from typing import Sequence

from domain.entities.client.value_objects import ClientID
from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleID
from domain.entities.user.value_objects import UserID


class RoleRepository(ABC):
    @abstractmethod
    async def save(self, role: Role) -> RoleID: ...

    @abstractmethod
    async def get_by_id(self, role_id: RoleID) -> Role | None: ...

    @abstractmethod
    async def get_roles_by_ids(
        self, role_ids: list[RoleID]
    ) -> Sequence[Role]: ...

    @abstractmethod
    async def get_roles_by_client_id(
        self, client_id: ClientID, order_by_id: bool = False
    ) -> Sequence[Role]: ...

    @abstractmethod
    async def get_base_client_roles(
        self, client_id: ClientID
    ) -> list[Role]: ...

    @abstractmethod
    async def get_user_roles_by_client_id(
        self, user_id: UserID, client_id: ClientID
    ) -> list[Role]: ...
