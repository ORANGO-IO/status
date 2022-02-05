"""job

Revision ID: 71efc1634150
Revises: 10d6acd6897a
Create Date: 2022-02-05 18:26:50.756668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71efc1634150'
down_revision = '10d6acd6897a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'job',
    sa.Column('id', sa.Integer(),unique=True),
    sa.Column('order', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('action', sa.String(), nullable=False),
    sa.Column('action_value', sa.String(), nullable=True),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime()),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], ondelete='cascade'),
     )


def downgrade():
    op.drop_table("job")
