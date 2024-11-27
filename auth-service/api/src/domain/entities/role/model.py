from dataclasses import dataclass, field

from domain.entities.role.value_objects import RoleID, RoleName


@dataclass
class Role:
    id: RoleID = field(init=False)
    name: RoleName
