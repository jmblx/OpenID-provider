from uuid import UUID, uuid4

from domain.common.services.pwd_service import PasswordHasher
from domain.entities.client.model import Client
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
    role_id: RoleID
    email: Email
    hashed_password: HashedPassword
    is_email_confirmed: bool
    permissions: RoleBaseScopes = field(init=False)
    clients: list[Client] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        user_id: UUID,
        role_id: int,
        email: str,
        raw_password: str,
        password_hasher: PasswordHasher,
        is_email_confirmed: bool = False,
    ) -> "User":
        return cls(
            id=UserID(user_id),
            role_id=RoleID(role_id),
            email=Email(email),
            hashed_password=password_hasher.hash_password(
                RawPassword(raw_password)
            ),
            is_email_confirmed=is_email_confirmed,
        )

    @staticmethod
    def generate_id() -> UUID:
        return uuid4()

    def check_pwd(
        self,
        plain_password: RawPassword,
        password_hasher: PasswordHasher,
    ) -> None:
        try:
            password_hasher.check_password(
                plain_password, self.hashed_password
            )
        except PasswordMismatchError as exc:
            raise InvalidCredentialsError from exc

    def confirm_email(self) -> None:
        self.is_email_confirmed = True

    def get_scopes(self) -> str:
        return f"user_{self.id.value}:111"
