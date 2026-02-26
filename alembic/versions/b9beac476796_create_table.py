"""create table

Revision ID: b9beac476796
Revises: 44815377283e
Create Date: 2026-02-26 22:33:55.427091
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b9beac476796'
down_revision: Union[str, Sequence[str], None] = '44815377283e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ✅ Explicit ENUM definition
bank_status_enum = postgresql.ENUM(
    'active',
    'inactive',
    name='bank_status_enum'
)


def upgrade() -> None:
    """Upgrade schema."""

    # 🔥 1️⃣ Create ENUM type first
    bank_status_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ Add new columns
    op.add_column(
        'banks',
        sa.Column(
            'status',
            bank_status_enum,
            server_default='active',
            nullable=True
        )
    )

    op.add_column(
        'banks',
        sa.Column('logo_url', sa.String(length=255), nullable=True)
    )

    # 3️⃣ Drop old column
    op.drop_column('banks', 'image_url')


def downgrade() -> None:
    """Downgrade schema."""

    # 1️⃣ Add image_url back
    op.add_column(
        'banks',
        sa.Column('image_url', sa.VARCHAR(length=255), nullable=True)
    )

    # 2️⃣ Drop new columns
    op.drop_column('banks', 'logo_url')
    op.drop_column('banks', 'status')

    # 🔥 3️⃣ Drop ENUM type
    bank_status_enum.drop(op.get_bind(), checkfirst=True)