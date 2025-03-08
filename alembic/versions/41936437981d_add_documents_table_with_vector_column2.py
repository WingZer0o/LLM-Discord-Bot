"""Add documents table with vector column2

Revision ID: 41936437981d
Revises: 
Create Date: 2025-03-07 21:22:16.220130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = '41936437981d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ChatMessages',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('Author', sa.String(length=250), nullable=False),
    sa.Column('IsBot', sa.Boolean(), nullable=False),
    sa.Column('CreatedAt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_table('Documents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=1536), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Documents')
    op.drop_table('ChatMessages')
    # ### end Alembic commands ###
