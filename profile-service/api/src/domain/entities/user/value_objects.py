from dataclasses import dataclass
import re
from datetime import datetime
from uuid import UUID, uuid4

from domain.exceptions.user_vo import (
    InvalidEmailError,
    InvalidUserIDError,
    InvalidRegisterDateError,
    InvalidFilePathError,
    InvalidCharacterError,
    EmptyValueError,
)


@dataclass(frozen=True)
class UserID:
    value: UUID

    @staticmethod
    def generate():
        return UserID(uuid4())
