from dataclasses import dataclass


@dataclass
class PKCEData:
    code_challenge: str
    code_challenge_method: str = "S256"
