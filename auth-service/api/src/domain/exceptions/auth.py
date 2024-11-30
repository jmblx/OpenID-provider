from dataclasses import dataclass

from application.common.exceptions import ApplicationError
from domain.common.exceptions.base import DomainError


@dataclass(eq=False)
class InvalidTokenError(ApplicationError): ...


@dataclass(eq=False)
class InvalidClientError(ApplicationError):
    @property
    def title(self) -> str:
        return "Invalid client."


@dataclass(eq=False)
class InvalidRedirectURLError(ApplicationError):
    redirect_url: str
    client_id: int

    @property
    def title(self) -> str:
        return f"{self.redirect_url} is not a valid redirect URL for client with id: {self.client_id}."


@dataclass(eq=False)
class InvalidCredentialsError(ApplicationError): ...
