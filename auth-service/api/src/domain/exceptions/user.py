from dataclasses import dataclass

from application.common.exceptions import ApplicationError
from domain.common.exceptions.base import DomainError


@dataclass(eq=False)
class UserNotFoundByIdError(DomainError):
    user_id: str

    @property
    def title(self) -> str:
        return f"User with id {self.user_id} not found."


@dataclass(eq=False)
class UserAlreadyExistsError(DomainError):
    email: str

    @property
    def title(self) -> str:
        return f"{self.email} is already registered."


@dataclass(eq=False)
class UserNotFoundByEmailError(DomainError):
    email: str

    @property
    def title(self) -> str:
        return f"{self.email} doesn't exists."
