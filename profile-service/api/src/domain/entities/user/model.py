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
    is_email_confirmed: bool

    @classmethod
    def create(
        cls,
        user_id: UUID,
        email: str,
        # is_email_confirmed: bool = False,
    ) -> "User":
        return cls(
            id=UserID(user_id),
            email=Email(email),
            # is_email_confirmed=is_email_confirmed,
        )

    def get_scopes(self) -> str:
        return f"user_{self.id.value}:111"
