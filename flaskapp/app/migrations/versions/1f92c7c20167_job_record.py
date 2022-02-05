"""job_record

Revision ID: 1f92c7c20167
Revises: 71efc1634150
Create Date: 2022-02-05 18:29:58.928369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f92c7c20167'
down_revision = '71efc1634150'
branch_labels = None
depends_on = None


def upgrade():
      op.create_table(
    'job_records',
    sa.Column('id', sa.Integer(),unique=True),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('time_spent_in_sec', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime()),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['status_id'], ['job_record_status.id'], ondelete='cascade'),
     )


def downgrade():
    op.drop_table("job_record")
