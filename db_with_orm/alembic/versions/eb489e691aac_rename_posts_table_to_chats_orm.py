"""rename posts table to chats_orm

Revision ID: eb489e691aac
Revises: 0105aacf5853
Create Date: 2025-11-30 09:29:13.598135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb489e691aac'
down_revision: Union[str, Sequence[str], None] = '0105aacf5853'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table('posts', 'chats_orm')
    pass


def downgrade() -> None:
    op.rename_table('chats_orm', 'posts')
    pass
