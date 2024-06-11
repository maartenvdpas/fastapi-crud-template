"""add user

Revision ID: 65d759f9d579
Revises: 
Create Date: 2024-06-11 11:14:24.799617

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65d759f9d579'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(320), index=True),
        sa.Column("password_hash", sa.String(128), nullable=True),
        sa.Column("registered_at", sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table("users")
