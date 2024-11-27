from dataclasses import dataclass, field


@dataclass
class RegisterUserCommand:
    email: str
    password: str
    redirect_url: str
    client_id: int
    code_challenge: str
    code_challenge_method: str = field(default="S256")
    role_id: int = field(default=1)
