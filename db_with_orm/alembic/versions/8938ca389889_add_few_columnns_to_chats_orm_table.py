"""add few columnns to chats_orm table

Revision ID: 8938ca389889
Revises: eb489e691aac
Create Date: 2025-11-30 09:33:22.886135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8938ca389889'
down_revision: Union[str, Sequence[str], None] = 'eb489e691aac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('chats_orm', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('chats_orm', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('chats_orm', 'published')
    op.drop_column('chats_orm', 'created_at')
    pass