from abc import ABC, abstractmethod
from typing import TypedDict

from domain.entities.resource_server.value_objects import ResourceServerID


class ResourceServerData(TypedDict):
    name: str


class ResourceServerReader(ABC):
    @abstractmethod
    async def get_resource_server_data_by_ids(self, rs_ids: list[ResourceServerID]) -> dict[ResourceServerID, ResourceServerData]: ...
