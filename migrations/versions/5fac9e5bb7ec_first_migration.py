"""first migration

Revision ID: 5fac9e5bb7ec
Revises: 
Create Date: 2021-11-03 22:57:30.534266

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5fac9e5bb7ec"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "bookrequests",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("isbn", sa.Integer, index=True),
        sa.Column("date", sa.DateTime),
    )
    pass


def downgrade():
    pass
