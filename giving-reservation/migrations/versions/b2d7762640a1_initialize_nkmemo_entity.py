"""Initialize

Revision ID: b2d7762640a1
Revises:
Create Date: 2022-03-25 00:16:22.752951

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b2d7762640a1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("title", sa.String(length=80), nullable=False, index=True),
        sa.Column("content", sa.Text, nullable=True),
        sa.Column("is_favorite", sa.Boolean, nullable=False),
    )


def downgrade():
    pass
