from dataclasses import dataclass

from application.resource_server.common.rs_repo import ResourceServerRepository
from application.common.uow import Uow
from domain.entities.resource_server.value_objects import ResourceServerID, ResourceServerType
from domain.exceptions.resource_server import ResourceServerNotFoundError


@dataclass
class UpdateResourceServerCommand:
    rs_id: int
    new_name: str | None
    new_type: ResourceServerType | None


class UpdateResourceServerHandler:
    def __init__(self, rs_repo: ResourceServerRepository, uow: Uow):
        self.rs_repo = rs_repo
        self.uow = uow

    async def handle(self, command: UpdateResourceServerCommand):
        rs = await self.rs_repo.get_by_id(ResourceServerID(command.rs_id))
        if not rs:
            raise ResourceServerNotFoundError()

        updates = {
            "name": (command.new_name if command.new_name else None),
            "type": (command.new_type if command.new_type else None),
        }

        for attr, value in updates.items():
            if value is not None:
                setattr(rs, attr, value)

        await self.rs_repo.save(rs)
        await self.uow.commit()
