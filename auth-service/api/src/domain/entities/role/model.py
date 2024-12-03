from dataclasses import dataclass, field

from domain.entities.client.value_objects import ClientID
from domain.entities.role.value_objects import (
    RoleID,
    RoleName,
    RoleBaseScopes,
)


@dataclass
class Role:
    id: RoleID = field(init=False)
    name: RoleName
    base_scopes: RoleBaseScopes
    client_id: ClientID

    @classmethod
    def create(cls, name: str, base_scopes: dict[str, str], client_id: int) -> "Role":
        return cls(name=RoleName(name), base_scopes=RoleBaseScopes.create(base_scopes), client_id=ClientID(client_id))
