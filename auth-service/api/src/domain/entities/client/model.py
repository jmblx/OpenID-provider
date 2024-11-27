from typing import Self

from domain.entities.client.value_objects import (
    ClientID,
    ClientType,
    ClientName,
    ClientBaseUrl,
    ClientRedirectUrl,
)

from dataclasses import dataclass, field

from infrastructure.db.models.client.client_models import client_table
from infrastructure.db.models.registry import mapper_registry


@dataclass
class Client:
    id: ClientID = field(init=False)
    name: ClientName
    base_url: ClientBaseUrl
    allowed_redirect_urls: list[ClientRedirectUrl]
    type: ClientType

    @classmethod
    def create(
        cls,
        name: ClientName,
        base_url: ClientBaseUrl,
        allowed_redirect_urls: list[ClientRedirectUrl],
        type: ClientType,
    ) -> Self:
        client = cls(name, base_url, allowed_redirect_urls, type)
        client._validate_urls()
        return client

    def _validate_urls(self) -> None:
        for url in self.allowed_redirect_urls:
            if self.base_url.value not in url.value:
                raise ValueError(
                    f"Base url {self.base_url.value} not in redirect url {url.value}"
                )


mapper_registry.map_imperatively(
    Client,
    client_table,
    properties={
        "id": client_table.c.id,
        "name": client_table.c.name,
        "base_url": client_table.c.base_url,
        "allowed_redirect_urls": client_table.c.allowed_redirect_urls,
        "type": client_table.c.type,
    },
)
