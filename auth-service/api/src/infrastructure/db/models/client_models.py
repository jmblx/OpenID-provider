import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import composite, relationship

from domain.entities.client.model import Client
from domain.entities.client.value_objects import (
    ClientTypeEnum,
    ClientName,
    ClientBaseUrl,
    ClientType,
    ClientID,
    AllowedRedirectUrls,
)
from infrastructure.db.models.registry import mapper_registry
from infrastructure.db.models.secondary import user_client_association_table

client_table = sa.Table(
    "client",
    mapper_registry.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("base_url", sa.String, nullable=False),
    sa.Column("allowed_redirect_url", ARRAY(sa.String), nullable=False),
    sa.Column(
        "type",
        sa.Enum(ClientTypeEnum, name="client_type_enum"),
        nullable=False,
    ),
)

mapper_registry.map_imperatively(
    Client,
    client_table,
    properties={
        "id": composite(ClientID, client_table.c.id),
        "name": composite(ClientName, client_table.c.name),
        "base_url": composite(ClientBaseUrl, client_table.c.base_url),
        "allowed_redirect_url": composite(
            AllowedRedirectUrls, client_table.c.allowed_redirect_url
        ),
        "type": composite(ClientType, client_table.c.type),
        "users": relationship(
            "User",
            secondary=user_client_association_table,
            back_populates="clients",
            uselist=True,
        ),
        "roles": relationship("Role", back_populates="client", uselist=True),
    },
    column_prefix="_",
)
