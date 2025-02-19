from uuid import UUID, uuid4

from domain.common.services.pwd_service import PasswordHasher
from domain.entities.client.model import Client
from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleID, RoleBaseScopes
from domain.entities.user.value_objects import (
    UserID,
    Email,
    HashedPassword,
    RawPassword,
)

from dataclasses import dataclass, field

from domain.exceptions.auth import InvalidCredentialsError
from domain.exceptions.pwd_hasher import PasswordMismatchError


@dataclass
class User:
    id: UserID
    email: Email
    is_email_confirmed: bool = field(default=False)
    avatar_path: str = field(default=None)

    @classmethod
    def create(
        cls,
        user_id: UUID,
        email: str,
        is_email_confirmed: bool = False,
        avatar_path: str = None,
    ) -> "User":
        return cls(
            id=UserID(user_id),
            email=Email(email),
            is_email_confirmed=is_email_confirmed,
            avatar_path=avatar_path,
        )

    @staticmethod
    def generate_id() -> UUID:
        return uuid4()

    def confirm_email(self) -> None:
        self.is_email_confirmed = True
