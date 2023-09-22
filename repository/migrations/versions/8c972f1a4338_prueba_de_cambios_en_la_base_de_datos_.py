# pylint: skip-file

"""Prueba de cambios en la base de datos, tratando de agregar una nueva tabla de following y cambiando atributos

Revision ID: 8c972f1a4338
Revises: 82ccb801ce64
Create Date: 2023-09-21 11:50:11.538863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8c972f1a4338"
down_revision: Union[str, None] = "82ccb801ce64"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
