import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.orm import relationship

from infrastructure.db.models.registry import metadata, mapper_registry
from infrastructure.db.models.user_models import UserDB

role_table = sa.Table(
    "role",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("permissions", sa.JSON),
)


class Role:
    def __init__(self, id: int, name: str, permissions: dict[str, int]):
        self.id = id
        self.name = name
        self.permissions = permissions

mapper_registry.map_imperatively(
    Role,
    role_table,
    properties={
        "users_role": relationship(UserDB, back_populates="role", uselist=True)
    },
)


# @event.listens_for(User, "load")
# def receive_load(target: User, _: ExecutionContext) -> None:
#     target.roles = set(target.roles) if isinstance(target.roles, list) else target.roles

