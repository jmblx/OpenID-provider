import uuid

from sqlalchemy import (
    Table,
    Column,
    Integer,
    UUID as SQLAlchemyUUID, Float,
)
from sqlalchemy.orm import relationship

from domain.entities.strategy.model import Strategy
from infrastructure.db.models.registry import mapper_registry
from infrastructure.db.models.secondary import user_strategy_association_table

strategy_table = Table(
    'strategy',
    mapper_registry.metadata,
Column("id", SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("budget", Float, nullable=False),
    Column("days_duration", Integer, nullable=False),
)

mapper_registry.map_imperatively(
    Strategy,
    strategy_table,
    properties={
        "users": relationship(
            "User",
            secondary=user_strategy_association_table,
            back_populates="strategies",
            uselist=True,
        ),
    }
)
