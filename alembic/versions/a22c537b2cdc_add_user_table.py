"""add user table

Revision ID: a22c537b2cdc
Revises: d5e6b92d2e5a
Create Date: 2025-01-12 13:17:48.793083

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a22c537b2cdc'
down_revision: Union[str, None] = 'd5e6b92d2e5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                     sa.Column('id', sa.Integer,nullable=False),
                     sa.Column('email', sa.String, nullable=False),
                     sa.Column('passsword', sa.String,nullable=False),
                     sa.Column('creayed-at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                     sa.PrimaryKeyConstraint('id'),
                     sa.UniqueConstraint('email')
                     )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
