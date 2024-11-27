import uuid
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from infrastructure.db.models.registry import metadata, mapper_registry

user_table = sa.Table(
    "user",
    metadata,
    sa.Column(
        "id", sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    ),
    sa.Column("email", sa.String, nullable=False),
    sa.Column("is_email_confirmed", sa.Boolean, default=False),
    sa.Column("hashed_password", sa.String, nullable=False),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("role.id"), default=1),
)


class UserDB:
    def __init__(
        self,
        id: uuid.UUID,
        email: str,
        is_email_confirmed: bool,
        hashed_password: str,
        role_id: int,
    ):
        self.id = id
        self.email = email
        self.is_email_confirmed = is_email_confirmed
        self.hashed_password = hashed_password
        self.role_id = role_id


mapper_registry.map_imperatively(
    UserDB,
    user_table,
    properties={
        "role": relationship("Role", back_populates="users_role", uselist=False)
    },
)
