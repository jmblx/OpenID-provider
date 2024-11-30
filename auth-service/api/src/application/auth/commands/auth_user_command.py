from dataclasses import dataclass

from application.auth.services.pkce import PKCECodeChallengeMethod


@dataclass
class AuthenticateUserCommand:
    email: str
    password: str
    redirect_url: str
    code_verifier: str
    code_challenge_method: PKCECodeChallengeMethod
    client_id: int
    scopes: list[str] | None
