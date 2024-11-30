from dataclasses import dataclass, field
from typing import Self, Union

from domain.entities.client.value_objects import (
    ClientID,
    ClientType,
    ClientName,
    ClientBaseUrl,
    AllowedRedirectUrls,
    ClientTypeEnum,
    ClientRedirectUrl,
)
from domain.exceptions.auth import InvalidRedirectURLError, InvalidClientError


@dataclass
class Client:
    id: ClientID = field(init=False)
    name: ClientName
    base_url: ClientBaseUrl
    allowed_redirect_urls: AllowedRedirectUrls
    type: ClientType

    @classmethod
    def create(
        cls,
        name: str,
        base_url: str,
        allowed_redirect_urls: list[str],
        type: ClientTypeEnum,
    ) -> Self:
        client = cls(
            ClientName(name),
            ClientBaseUrl(base_url),
            AllowedRedirectUrls(allowed_redirect_urls),
            ClientType(type),
        )
        return client

    @staticmethod
    async def validate_redirect_url(
        client: Union["Client", None],
        redirect_url: ClientRedirectUrl,
    ) -> None:
        if not client:
            raise InvalidClientError()

        if redirect_url.value not in client.allowed_redirect_urls.value:
            raise InvalidRedirectURLError(
                redirect_url=redirect_url.value, client_id=client.id.value
            )
