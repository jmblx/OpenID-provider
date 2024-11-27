from dataclasses import dataclass


@dataclass
class AuthenticateUserCommand:
    email: str
    password: str
