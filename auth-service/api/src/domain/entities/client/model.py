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
    def validate_redirect_url(
        allowed_redirect_urls: "AllowedRedirectUrls",
        redirect_url: ClientRedirectUrl,
    ) -> None:
        for allowed_redirect_url in allowed_redirect_urls.value:
            if redirect_url.value in allowed_redirect_url.replace("/{auth_code}", "") or redirect_url.value in allowed_redirect_url:
                return
            raise InvalidRedirectURLError(
                redirect_url=redirect_url.value
            )

    def rename(self, name: str) -> None:
        self.name = ClientName(name)

    def add_allowed_redirect_url(self, new_allowed_redirect_url: str) -> None:
        self.allowed_redirect_urls = AllowedRedirectUrls(self.allowed_redirect_urls.value + [ClientRedirectUrl(new_allowed_redirect_url).value])
