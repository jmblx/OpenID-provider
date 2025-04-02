from dataclasses import dataclass
from typing import TypedDict

from application.common.views.role_view import RoleViewWithId
from domain.entities.resource_server.value_objects import ResourceServerType


class ResourceServerView(TypedDict, total=False):
    name: str
    type: ResourceServerType
    roles: list[RoleViewWithId]


@dataclass
class ResourceServersIdsData:
    name: str
