from uuid import UUID, uuid4

from domain.entities.user.value_objects import (
    UserID,
    Email,
    HashedPassword,
    RawPassword,
)

from dataclasses import dataclass, field

@dataclass
class User:
    id: UserID
    email: Email
    avatar_path: str = field(default=None)

    @classmethod
    def create(
        cls,
        user_id: UUID,
        email: str,
        avatar_path: str = None,
    ) -> "User":
        return cls(
            id=UserID(user_id),
            email=Email(email),
            avatar_path=avatar_path,
        )

    @staticmethod
    def generate_id() -> UUID:
        return uuid4()

    def confirm_email(self) -> None:
        self.is_email_confirmed = True
