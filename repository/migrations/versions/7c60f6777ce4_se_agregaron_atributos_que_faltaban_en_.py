# pylint: skip-file

"""Se agregaron atributos que faltaban en la tabla de usuarios, y se creo una nueva tabla following.

Revision ID: 7c60f6777ce4
Revises: 84d667de3693
Create Date: 2023-09-21 12:07:38.297472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c60f6777ce4"
down_revision: Union[str, None] = "84d667de3693"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
