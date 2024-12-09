from dataclasses import dataclass


@dataclass
class CreateRoleCommand:
    name: str
    base_scopes: dict[str, str]
    client_id: int
