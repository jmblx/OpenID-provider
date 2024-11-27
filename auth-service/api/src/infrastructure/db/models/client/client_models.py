import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY

from domain.entities.client.value_objects import ClientTypeEnum
from infrastructure.db.models.registry import metadata

client_table = sa.Table(
    "client",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("name", sa.String, nullable=False),
    sa.Column("base_url", sa.String, nullable=False),
    sa.Column("allowed_redirect_urls", ARRAY(sa.String), nullable=False),
    sa.Column(
        "type",
        sa.Enum(ClientTypeEnum, name="client_type_enum"),
        nullable=False,
    ),
)
