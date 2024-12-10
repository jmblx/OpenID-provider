from dataclasses import dataclass

from domain.common.exceptions.base import DomainError


class ClientNameLengthError(DomainError): ...


@dataclass(eq=False)
class InvalidUrlError(DomainError):
    details: str

    @property
    def title(self) -> str:
        return f"Client not found. Deatails: {self.details}"


@dataclass(eq=False)
class ClientNotFound(DomainError):

    @property
    def title(self) -> str:
        return f"Client not found"
