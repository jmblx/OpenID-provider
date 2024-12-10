from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.client.value_objects import ClientID


@dataclass
class ClientAuthData:
    client_name: str
    allowed_redirect_urls: list[str]


class ClientReader(ABC):
    @abstractmethod
    async def read_for_auth_page(
        self, client_id: ClientID
    ) -> ClientAuthData | None: ...
