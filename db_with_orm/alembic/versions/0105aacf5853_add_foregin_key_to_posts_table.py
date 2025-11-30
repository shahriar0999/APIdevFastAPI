"""add foregin-key to posts table

Revision ID: 0105aacf5853
Revises: 8d03231443bd
Create Date: 2025-11-30 09:20:30.795562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0105aacf5853'
down_revision: Union[str, Sequence[str], None] = '8d03231443bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
