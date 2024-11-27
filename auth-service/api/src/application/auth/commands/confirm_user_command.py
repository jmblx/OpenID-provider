from dataclasses import dataclass


@dataclass
class ConfirmUserCommand:
    confirmation_code: str
