import sqlalchemy as sa
from sqlalchemy.orm import relationship

from domain.entities.resource_server.model import ResourceServer
from domain.entities.resource_server.value_objects import ResourceServerType
from infrastructure.db.models.registry import mapper_registry
from infrastructure.db.models.secondary import client_rs_association_table, user_rs_association_table

rs_table = sa.Table(
    "resource_server",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column(
        "type",
        sa.Enum(ResourceServerType, name="access_control_type_enum"),
        nullable=False,
    ),
)

mapper_registry.map_imperatively(
    ResourceServer,
    rs_table,
    properties={
        "id": rs_table.c.id,
        "name": rs_table.c.name,
        "type": rs_table.c.type,
        # "clients": relationship("Client", secondary=client_rs_association_table, back_populates="resource_servers", uselist=True),
        "roles": relationship(
            "Role", back_populates="resource_server", uselist=True
        ),
        "users_rss": relationship("User", back_populates="resource_servers", uselist=True, secondary=user_rs_association_table),
    },
    column_prefix="_",
)
