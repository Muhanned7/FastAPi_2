"""create posts table

Revision ID: 785ec13d6f20
Revises: 
Create Date: 2025-01-12 10:08:38.865055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '785ec13d6f20'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False,primary_key=True), 
        sa.Column('Title', sa.String(50), nullable=False))
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
