from sqlalchemy import Table, Column, ForeignKey
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from infrastructure.db.models.registry import mapper_registry

user_client_association_table = Table(
    "user_client_association",
    mapper_registry.metadata,
    Column("id", sa.Integer, primary_key=True, autoincrement=True),
    Column("user_id", PGUUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("client_id", sa.Integer, ForeignKey("client.id"), nullable=False),
)
