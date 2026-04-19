"""add category to selections

Revision ID: a3f9c2d1e5b7
Revises: 2461628084b0
Create Date: 2026-04-19 00:00:00.000000

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa

revision: str = 'a3f9c2d1e5b7'
down_revision: Union[str, Sequence[str], None] = '2461628084b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('selections', sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('selections', 'category')
