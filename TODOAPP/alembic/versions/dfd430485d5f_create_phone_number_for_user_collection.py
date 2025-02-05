"""Create phone number for user collection

Revision ID: dfd430485d5f
Revises: 
Create Date: 2025-02-05 17:13:18.745612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dfd430485d5f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(15), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "phone_number")
