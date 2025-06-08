from dataclasses import dataclass, field
from datetime import datetime
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
from domain.exceptions.auth import InvalidRedirectURLError


@dataclass
class Client:
    id: ClientID = field(init=False)
    name: ClientName
    base_url: ClientBaseUrl
    allowed_redirect_urls: AllowedRedirectUrls
    type: ClientType
    search_name: str
    avatar_upd_at: datetime

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
            cls.make_search_name(name, base_url)
        )
        return client

    @staticmethod
    def validate_redirect_url(
        allowed_redirect_urls: "AllowedRedirectUrls",
        redirect_url: ClientRedirectUrl,
    ) -> None:
        if redirect_url.value in allowed_redirect_urls.value:
            return
        raise InvalidRedirectURLError(redirect_url=redirect_url.value)

    def rename(self, name: str) -> None:
        self.name = ClientName(name)

    def add_allowed_redirect_url(self, new_allowed_redirect_url: str) -> None:
        self.allowed_redirect_urls = AllowedRedirectUrls(
            self.allowed_redirect_urls.value
            + [ClientRedirectUrl(new_allowed_redirect_url).value]
        )

    @staticmethod
    def make_search_name(name: str, base_url: str | None) -> str:
        """
        Объединяет name и base_url в строку для поиска, приводя к нижнему регистру.
        """
        base_url = base_url or ""
        return f"{name.strip().lower()} {base_url.strip()}".lower()
