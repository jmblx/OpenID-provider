from dataclasses import dataclass


@dataclass(frozen=True)
class AuthenticateUserCommand:
    redirect_uri: str
    code_verifier: str
