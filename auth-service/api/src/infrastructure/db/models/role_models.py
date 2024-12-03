from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, composite

from domain.entities.role.model import Role
from domain.entities.role.value_objects import RoleID, RoleName, RoleBaseScopes
from infrastructure.db.models.registry import mapper_registry

role_table = Table(
    "role",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("base_scopes", JSONB, nullable=False),
    Column("client_id", Integer, ForeignKey("client.id"), nullable=False),
)

mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={
        "id": composite(RoleID, role_table.c.id),
        "name": composite(RoleName, role_table.c.name),
        "base_scopes": composite(RoleBaseScopes, role_table.c.base_scopes),
        "users_role": relationship(
            "User",
            back_populates="role",
            uselist=True,
        ),
        "client_id": composite(RoleID, role_table.c.client_id),
        "client": relationship("Client", back_populates="roles", uselist=False),
    },
    column_prefix="_",
)
