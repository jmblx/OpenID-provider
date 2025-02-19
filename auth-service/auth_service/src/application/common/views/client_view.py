from dataclasses import dataclass
from typing import TypedDict

from application.common.views.role_view import RoleViewWithId
from domain.entities.client.value_objects import ClientTypeEnum


class ClientView(TypedDict, total=False):
    name: str
    base_url: str
    allowed_redirect_urls: list[str]
    type: ClientTypeEnum
    roles: list[RoleViewWithId]


@dataclass
class ClientsIdsData:
    name: str
