"""service_groups

Revision ID: 162ff8545ab8
Revises: 
Create Date: 2022-02-05 18:05:56.913484

"""
from enum import unique
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '162ff8545ab8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
    'service_groups',
    sa.Column('id', sa.Integer(),unique=True),
    sa.Column('name', sa.String(), nullable=False,unique=True),
    sa.Column('created_at', sa.DateTime()),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table("service_groups")
