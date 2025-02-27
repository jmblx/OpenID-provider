from sqlalchemy import (
    Table,
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
    UUID as SQLAlchemyUUID,
)
from sqlalchemy.orm import relationship, composite

from domain.entities.role.value_objects import RoleID
from domain.entities.user.model import User
from domain.entities.user.value_objects import UserID, Email, HashedPassword
from infrastructure.db.models.registry import mapper_registry
from infrastructure.db.models.secondary import (
    user_client_association_table,
    user_role_association, user_rs_association_table,
)

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("id", SQLAlchemyUUID(as_uuid=True), primary_key=True),
    Column("email", String, nullable=False),
    Column("is_email_confirmed", Boolean, default=False),
    Column("hashed_password", String, nullable=False),
    Column("avatar_path", String, nullable=True),
)

mapper_registry.map_imperatively(
    User,
    user_table,
    properties={
        "id": composite(UserID, user_table.c.id),
        "email": composite(Email, user_table.c.email),
        "hashed_password": composite(
            HashedPassword, user_table.c.hashed_password
        ),
        "is_email_confirmed": user_table.c.is_email_confirmed,
        "avatar_path": user_table.c.avatar_path,
        "roles": relationship(
            "Role",
            secondary=user_role_association,
            back_populates="users_roles",
            uselist=True,
        ),
        "resource_servers": relationship("ResourceServer", uselist=True, back_populates="users_rss", secondary=user_rs_association_table),
        # "clients": relationship(
        #     "Client",
        #     secondary=user_client_association_table,
        #     back_populates="users",
        #     uselist=True,
        # ),
    },
    column_prefix="_",
)
