"""add all columns to posts

Revision ID: eb707d3a6bbb
Revises: 2edda529011e
Create Date: 2025-01-12 15:01:10.538002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb707d3a6bbb'
down_revision: Union[str, None] = '2edda529011e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published', sa.Boolean, nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at',sa.TIMESTAMP(timezone=False),nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
    pass
