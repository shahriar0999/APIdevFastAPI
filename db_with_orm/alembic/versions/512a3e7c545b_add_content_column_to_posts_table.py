"""add content column to posts table

Revision ID: 512a3e7c545b
Revises: 95c7102d2bd1
Create Date: 2025-11-30 09:06:47.787044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '512a3e7c545b'
down_revision: Union[str, Sequence[str], None] = '95c7102d2bd1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
