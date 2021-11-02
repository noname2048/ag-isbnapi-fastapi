"""Initialize Isbn entity

Revision ID: 88f2d2a8d7d0
Revises: 
Create Date: 2021-11-02 23:24:29.995435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "88f2d2a8d7d0"
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


def downgrade():
    op.drop_table("bookrequests")
