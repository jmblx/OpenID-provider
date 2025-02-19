from sqlalchemy import Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, composite

from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleName, RoleBaseScopes
from infrastructure.db.models.registry import mapper_registry
from infrastructure.db.models.secondary import user_role_association

role_table = Table(
    "role",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("base_scopes", JSONB, nullable=False),
    Column("client_id", Integer, ForeignKey("client.id"), nullable=False),
    Column("is_base", Boolean, nullable=False),
)


mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={
        "id": role_table.c.id,
        "name": composite(RoleName, role_table.c.name),
        "base_scopes": composite(RoleBaseScopes, role_table.c.base_scopes),
        "users_roles": relationship(
            "User",
            secondary=user_role_association,
            back_populates="roles",
            uselist=True,
        ),
        "client_id": role_table.c.client_id,
        "client": relationship(
            "Client", back_populates="roles", uselist=False
        ),
        "is_base": role_table.c.is_base,
    },
    column_prefix="_",
)
