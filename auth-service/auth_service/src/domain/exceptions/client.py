from dataclasses import dataclass

from domain.common.exceptions.base import DomainError


@dataclass
class ClientNameLengthError(DomainError):
    details: str

    @property
    def title(self) -> str:
        return f"{self.details}"


@dataclass(eq=False)
class InvalidUrlError(DomainError):
    details: str

    @property
    def title(self) -> str:
        return f"{self.details}"


@dataclass(eq=False)
class ClientNotFound(DomainError):

    @property
    def title(self) -> str:
        return "Client not found"
