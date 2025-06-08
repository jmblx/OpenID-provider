from dataclasses import dataclass
from typing import TypedDict

from domain.entities.client.value_objects import ClientTypeEnum


class ClientData(TypedDict, total=False):
    name: str
    base_url: str
    allowed_redirect_urls: list[str]
    type: ClientTypeEnum

class ClientView(ClientData, total=False):
    avatar_url: str


@dataclass
class ClientsIdsData:
    name: str
