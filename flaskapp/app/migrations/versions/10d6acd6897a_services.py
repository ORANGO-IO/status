"""services

Revision ID: 10d6acd6897a
Revises: ad0406ddb474
Create Date: 2022-02-05 18:20:34.114089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10d6acd6897a'
down_revision = 'ad0406ddb474'
branch_labels = None
depends_on = None


def upgrade(): 
    op.create_table(
    'services',
    sa.Column('id', sa.Integer(),unique=True),
    sa.Column('name', sa.String(), nullable=False,unique=True),
    sa.Column('service_group_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime()),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['service_group_id'], ['service_groups.id'], ondelete='cascade'),
     )


def downgrade():
    op.drop_table("services")
