"""updated table coordinator

Revision ID: 4800f54233b6
Revises: e991595220f2
Create Date: 2026-03-05 13:33:21.544271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4800f54233b6'
down_revision: Union[str, Sequence[str], None] = 'e991595220f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        'coordinator_profiles',
        'experience',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="experience::integer"
    )

def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        'coordinator_profiles',
        'experience',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
        postgresql_using="experience::text"
    )