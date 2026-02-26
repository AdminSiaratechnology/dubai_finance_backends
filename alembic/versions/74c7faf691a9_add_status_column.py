"""add status column

Revision ID: 74c7faf691a9
Revises: dd25043d8db9
Create Date: 2026-02-26 11:00:56.305265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74c7faf691a9'
down_revision: Union[str, Sequence[str], None] = 'dd25043d8db9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # 1️⃣ Create Enum type in PostgreSQL first
    loan_status_enum = sa.Enum('active', 'inactive', name='loan_status_enum')
    loan_status_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ Add Column
    op.add_column(
        'loan_types',
        sa.Column(
            'status',
            loan_status_enum,
            nullable=True,          # initially True for safe migration
            server_default="active" # default for existing/empty rows
        )
    )

def downgrade() -> None:
    """Downgrade schema."""
    # 1️⃣ Drop column
    op.drop_column('loan_types', 'status')

    # 2️⃣ Drop Enum type
    loan_status_enum = sa.Enum('active', 'inactive', name='loan_status_enum')
    loan_status_enum.drop(op.get_bind(), checkfirst=True)