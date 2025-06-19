from dataclasses import dataclass
from enum import IntEnum
from typing import NewType

from domain.exceptions.client import ClientNameLengthError, InvalidUrlError

# @dataclass(frozen=True)
# class ClientID:
#     value: int
ClientID = NewType("ClientID", int)


class ClientTypeEnum(IntEnum):
    PUBLIC = 1
    PRIVATE = 2


@dataclass(frozen=True)
class ClientType:
    value: ClientTypeEnum

    def __post_init__(self) -> None: ...


@dataclass(frozen=True)
class ClientName:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("value must be an instance of str")
        self.check_length()

    def check_length(self) -> None:
        if len(self.value) > 100:
            raise ClientNameLengthError(
                "value must be less than 100 characters"
            )


def check_is_valid_url(url: str) -> None:
    if "://" not in url:
        raise InvalidUrlError("Invalid URL")


@dataclass(frozen=True)
class ClientBaseUrl:
    value: str

    def __post_init__(self) -> None:
        check_is_valid_url(self.value)


@dataclass(frozen=True)
class ClientRedirectUrl:
    value: str

    def __post_init__(self) -> None:
        check_is_valid_url(self.value)


@dataclass(frozen=True)
class AllowedRedirectUrls:
    value: list[str]

    def __post_init__(self) -> None:
        for url in self.value:
            check_is_valid_url(url)
