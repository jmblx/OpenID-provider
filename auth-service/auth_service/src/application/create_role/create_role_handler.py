from dataclasses import dataclass

from application.common.uow import Uow
from application.common.interfaces.role_repo import RoleRepository
from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleID


@dataclass
class CreateRoleCommand:
    name: str
    base_scopes: dict[str, str]
    client_id: int


class CreateRoleHandler:
    def __init__(self, role_repo: RoleRepository, uow: Uow) -> None:
        self.role_repo = role_repo
        self.uow = uow

    async def handle(self, command: CreateRoleCommand) -> int:
        role = Role.create(
            name=command.name,
            base_scopes=command.base_scopes,
            client_id=command.client_id,
        )
        role_id: RoleID = await self.role_repo.save(role)
        await self.uow.commit()
        return role_id.value
