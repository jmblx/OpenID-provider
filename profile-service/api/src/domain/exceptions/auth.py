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

    @property
    def title(self) -> str:
        return f"{self.redirect_url} is not a valid redirect URL for your client."


@dataclass(eq=False)
class InvalidCredentialsError(DomainError):
    @property
    def title(self) -> str:
        return "Invalid credentials."
