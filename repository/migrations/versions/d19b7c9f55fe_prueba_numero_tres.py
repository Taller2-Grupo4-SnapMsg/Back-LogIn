# pylint: skip-file

"""Prueba numero tres

Revision ID: d19b7c9f55fe
Revises: a09971c0a949
Create Date: 2023-09-21 12:02:11.094869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d19b7c9f55fe"
down_revision: Union[str, None] = "a09971c0a949"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
