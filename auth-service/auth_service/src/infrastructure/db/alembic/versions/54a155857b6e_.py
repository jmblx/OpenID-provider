"""empty message

Revision ID: 54a155857b6e
Revises: c106fbbffc38
Create Date: 2025-01-30 21:25:30.283052

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "54a155857b6e"
down_revision: Union[str, None] = "c106fbbffc38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("role", sa.Column("is_base", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("role", "is_base")
    # ### end Alembic commands ###
