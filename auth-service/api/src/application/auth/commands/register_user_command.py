from dataclasses import dataclass, field

from application.auth.services.pkce import PKCECodeChallengeMethod


@dataclass
class RegisterUserCommand:
    email: str
    password: str
    redirect_url: str
    client_id: int
    code_verifier: str
    code_challenge_method: PKCECodeChallengeMethod
    scopes: list[str] | None
    role_id: int = field(default=1)
