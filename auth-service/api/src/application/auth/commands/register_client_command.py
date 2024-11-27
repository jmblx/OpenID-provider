from dataclasses import dataclass

from domain.entities.client.value_objects import ClientType, ClientTypeEnum


@dataclass
class RegisterClientCommand:
    name: str
    base_url: str
    allowed_redirect_urls: list[str]
    type: ClientTypeEnum
