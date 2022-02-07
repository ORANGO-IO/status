"""screenshots

Revision ID: 81d72db256ea
Revises: 1f92c7c20167
Create Date: 2022-02-05 18:35:37.821874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81d72db256ea'
down_revision = '1f92c7c20167'
branch_labels = None
depends_on = None


def upgrade():
     op.create_table(
    'screenshots',
        sa.Column('id', sa.Integer(),unique=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('mime_type', sa.String(), nullable=False),
        sa.Column('job_record_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['job_record_id'], ['job_records.id'], ondelete='cascade'),
     )


def downgrade():
    
    op.drop_table("screenshots")
