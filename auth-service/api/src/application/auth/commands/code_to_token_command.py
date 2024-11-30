from dataclasses import dataclass


@dataclass
class CodeToTokenCommand:
    auth_code: str
    code_challenger: str
    redirect_url: str
    scopes: list[str]
