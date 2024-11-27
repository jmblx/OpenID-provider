from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserCreateOutputDTO:
    user_id: UUID
