"""add content columns to post table

Revision ID: d5e6b92d2e5a
Revises: 785ec13d6f20
Create Date: 2025-01-12 13:00:48.647360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5e6b92d2e5a'
down_revision: Union[str, None] = '785ec13d6f20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
