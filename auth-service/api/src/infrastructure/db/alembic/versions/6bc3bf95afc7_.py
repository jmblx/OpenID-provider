"""empty message

Revision ID: 6bc3bf95afc7
Revises: 48632ebf1ff4
Create Date: 2024-12-20 19:28:41.550525

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6bc3bf95afc7'
down_revision: Union[str, None] = '48632ebf1ff4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Проверяем, существует ли колонка `new_allowed_redirect_url`
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'client' AND column_name = 'new_allowed_redirect_url'
        """)
    ).fetchone()

    # Если колонка существует, переименовываем её
    if result:
        op.alter_column('client', 'new_allowed_redirect_url', new_column_name='allowed_redirect_urls')


def downgrade() -> None:
    # Обратное действие: переименовать обратно, если нужно
    conn = op.get_bind()
    result = conn.execute(
        sa.text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'client' AND column_name = 'allowed_redirect_urls'
        """)
    ).fetchone()

    if result:
        op.alter_column('client', 'allowed_redirect_urls', new_column_name='new_allowed_redirect_url')
