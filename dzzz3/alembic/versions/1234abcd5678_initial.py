"""initial

Revision ID: 1234abcd5678
Revises: 
Create Date: 2024-05-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '1234abcd5678'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('student_grades',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('faculty', sa.String(length=20), nullable=False),
    sa.Column('subject', sa.String(length=100), nullable=False),
    sa.Column('grade', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('student_grades')
