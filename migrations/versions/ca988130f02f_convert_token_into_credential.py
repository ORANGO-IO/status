"""convert token into credential

Revision ID: ca988130f02f
Revises: 262737ce338c
Create Date: 2025-05-14 06:12:32.193398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ca988130f02f'
down_revision = '262737ce338c'
branch_labels = None
depends_on = None


def upgrade():
    # Rename existing tokens table to credentials
    op.rename_table('tokens', 'credentials')

    # Adjust columns within renamed table
    with op.batch_alter_table('credentials', schema=None) as batch_op:
        # Rename column token -> secret
        batch_op.alter_column(
            'token', new_column_name='secret',
            existing_type=sa.VARCHAR(length=128),
            type_=sa.String(length=128),
            existing_nullable=False
        )
        # Rename existing 'type' column to 'system' (holds old token type values)
        batch_op.alter_column(
            'type', new_column_name='system',
            existing_type=sa.Enum('webhook', 'api', 'cli', 'master', name='token_type'),
            type_=sa.Enum('webhook', 'api', 'cli', 'master', 'external', name='credential_system'),
            existing_nullable=False
        )
        # Add new 'role' column (token or password)
        batch_op.add_column(sa.Column(
            'role',
            sa.Enum('token', 'password', name='credential_role'),
            nullable=False,
            server_default='token'
        ))
        # Alter service_id to be nullable
        batch_op.alter_column(
            'service_id',
            existing_type=mysql.CHAR(length=36),
            nullable=True
        )
        # Create unique constraint on secret
        batch_op.create_unique_constraint('uq_credentials_secret', ['secret'])

    # ### end Alembic commands ###


def downgrade():
    # Rename credentials back to tokens
    op.rename_table('credentials', 'tokens')

    # Adjust columns in renamed table
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        # Rename column secret -> token
        batch_op.alter_column(
            'secret', new_column_name='token',
            existing_type=sa.String(length=128),
            type_=mysql.VARCHAR(length=128),
            existing_nullable=False
        )
        # Rename column system -> type with original ENUM
        batch_op.alter_column(
            'system', new_column_name='type',
            existing_type=sa.Enum('webhook', 'api', 'cli', 'master', 'external', name='credential_system'),
            type_=mysql.ENUM('webhook', 'api', 'cli', 'master', name='token_type'),
            existing_nullable=False
        )
        # Drop added column role
        batch_op.drop_column('role')
        # service_id back to non-nullable
        batch_op.alter_column(
            'service_id',
            existing_type=mysql.CHAR(length=36),
            nullable=False
        )
        # Recreate old index on token
        batch_op.create_index('token', ['token'], unique=True)

    # ### end Alembic commands ###
