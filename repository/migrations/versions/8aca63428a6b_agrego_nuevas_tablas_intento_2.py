# pylint: skip-file
"""agrego nuevas tablas (intento 2)

Revision ID: 8aca63428a6b
Revises: 1551e9c3c188
Create Date: 2023-10-05 14:38:48.820362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8aca63428a6b"
down_revision: Union[str, None] = "1551e9c3c188"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the 'posts' table
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("posted_at", sa.DateTime(), default=sa.func.now(), nullable=True),
        sa.Column("content", sa.String(length=800), nullable=True),
        sa.Column("image", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create the 'likes' table
    op.create_table(
        "likes",
        sa.Column("id_post", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["id_post"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id_post", "user_id"),
    )


def downgrade() -> None:
    # Drop the 'likes' table
    op.drop_table("likes")

    # Drop the 'posts' table
    op.drop_table("posts")
