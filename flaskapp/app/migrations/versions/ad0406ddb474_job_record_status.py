"""job_record_status

Revision ID: ad0406ddb474
Revises: 162ff8545ab8
Create Date: 2022-02-05 18:18:25.340948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad0406ddb474'
down_revision = '162ff8545ab8'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
    'job_record_status',
    sa.Column('id', sa.Integer(),unique=True),
    sa.Column('value', sa.String(), nullable=False,unique=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
     )


def downgrade():
    op.drop_table("job_record_status")
