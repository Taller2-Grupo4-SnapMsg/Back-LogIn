# pylint: skip-file
"""se agrega la columna de is_public en la tabla de usuarios y se saca de la tabla de posts

Revision ID: fb0240b2bd48
Revises: 79f97b454224
Create Date: 2023-10-12 18:12:20.929219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "fb0240b2bd48"
down_revision: Union[str, None] = "79f97b454224"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "is_public")
    op.drop_column("posts", "is_public")
    # ### end Alembic commands ###
