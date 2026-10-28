"""add bio and is_verified columns to users

Revision ID: 002_add_profile
Revises: 001_initial
Create Date: 2026-10-28 10:15:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '002_add_profile'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns to existing users table
    op.add_column('users', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), server_default='0', nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'is_verified')
    op.drop_column('users', 'bio')
