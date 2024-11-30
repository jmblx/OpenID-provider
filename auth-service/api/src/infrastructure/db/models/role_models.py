from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from domain.entities.role.model import Role
from infrastructure.db.models.registry import mapper_registry

# Таблица role
role_table = Table(
    "role",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSONB, nullable=False),
)

# Маппинг
mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={
        "id": role_table.c.id,
        "name": role_table.c.name,
        "permissions": role_table.c.permissions,
        "users_role": relationship(
            "User",
            back_populates="role",  # Связь с пользователями
            uselist=True,
        ),
    },
)
