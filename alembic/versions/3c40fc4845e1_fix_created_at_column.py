"""fix created at column

Revision ID: 3c40fc4845e1
Revises: a22c537b2cdc
Create Date: 2025-01-12 14:06:30.341190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c40fc4845e1'
down_revision: Union[str, None] = 'a22c537b2cdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('users', column_name='creayed-at',new_column_name="created_at" )
    pass


def downgrade() -> None:
    op.alter_column('users', column_name='created_at',new_column_name="creayed_at" )
    pass
