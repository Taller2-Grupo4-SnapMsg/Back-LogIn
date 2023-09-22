# pylint: skip-file

"""Prueba numero dosss

Revision ID: a09971c0a949
Revises: 8c972f1a4338
Create Date: 2023-09-21 11:59:34.540367

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a09971c0a949"
down_revision: Union[str, None] = "8c972f1a4338"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
