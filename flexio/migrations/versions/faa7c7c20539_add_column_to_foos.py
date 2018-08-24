import sqlalchemy as sa

from alembic import op

from lib.util_datetime import tzware_datetime
from lib.util_sqlalchemy import AwareDateTime


"""
add column to foos

Revision ID: faa7c7c20539
Revises: 9e1affdfb1c5
Create Date: 2018-08-24 19:00:21.809634
"""

# Revision identifiers, used by Alembic.
revision = 'faa7c7c20539'
down_revision = '9e1affdfb1c5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('foos', sa.Column('hello_on', AwareDateTime(),
                                    default=tzware_datetime))


def downgrade():
    op.drop_column('foos', 'hello_on')
