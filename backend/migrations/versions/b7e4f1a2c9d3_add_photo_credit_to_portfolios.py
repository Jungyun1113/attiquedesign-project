"""add photo_credit to portfolios

Revision ID: b7e4f1a2c9d3
Revises: a3f9c2d1e5b7
Create Date: 2026-04-28 00:00:00.000000

"""
from typing import Sequence, Union

import sqlmodel
from alembic import op
import sqlalchemy as sa

revision: str = 'b7e4f1a2c9d3'
down_revision: Union[str, Sequence[str], None] = 'a3f9c2d1e5b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('portfolios', sa.Column('photo_credit', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('portfolios', 'photo_credit')
