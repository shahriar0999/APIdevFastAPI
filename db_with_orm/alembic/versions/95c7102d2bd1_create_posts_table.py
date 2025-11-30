"""create posts table

Revision ID: 95c7102d2bd1
Revises: 
Create Date: 2025-11-30 08:47:19.447876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95c7102d2bd1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
