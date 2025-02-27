from dataclasses import dataclass, field
from typing import Self

from domain.entities.resource_server.value_objects import (
    ResourceServerType,
    ResourceServerID,
)


@dataclass
class ResourceServer:
    id: ResourceServerID = field(init=False)
    name: str
    type: ResourceServerType

    @classmethod
    def create(
        cls,
        name: str,
        type: ResourceServerType,
    ) -> Self:
        resource_server = cls(
            name,
            type,
        )
        return resource_server

    def rename(self, name: str) -> None:
        self.name = name
