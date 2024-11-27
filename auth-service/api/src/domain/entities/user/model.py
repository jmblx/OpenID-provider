from domain.entities.role.value_objects import RoleID
from domain.entities.user.value_objects import UserID, Email, HashedPassword

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class User:
    id: "UserID" = field(init=False)
    role_id: "RoleID"
    email: "Email"
    hashed_password: HashedPassword
    is_email_confirmed: bool = field(init=False)

    @property
    def id_value(self) -> UUID:
        return self.id.value

    @property
    def email_value(self) -> str:
        return self.email.value

    @property
    def role_id_value(self) -> int:
        return self.role_id.value

    def check_password(self, password: str, hash_service) -> bool:
        return hash_service.check_password(
            password, self.hashed_password.value
        )

    def confirm_email(self):
        self.is_email_confirmed = True

    def get_scopes(self) -> str:
        return f"user_{self.id.value}:111"
