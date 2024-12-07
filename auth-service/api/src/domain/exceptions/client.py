from dataclasses import dataclass

from domain.common.exceptions.base import DomainError


class ClientNameLengthError(DomainError): ...


class InvalidUrlError(DomainError): ...

@dataclass(eq=False)
class ClientNotFound(DomainError):

    @property
    def title(self) -> str:
        return f"Client not found"
