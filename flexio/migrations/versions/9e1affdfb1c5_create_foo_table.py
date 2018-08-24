import sqlalchemy as sa

from alembic import op

from lib.util_datetime import tzware_datetime
from lib.util_sqlalchemy import AwareDateTime


"""
create foo table

Revision ID: 9e1affdfb1c5
Revises: 
Create Date: 2018-08-24 18:17:06.172615
"""

# Revision identifiers, used by Alembic.
revision = '9e1affdfb1c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('foos',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('created_on', AwareDateTime(),
                              default=tzware_datetime),
                    sa.Column('updated_on', AwareDateTime(),
                              default=tzware_datetime,
                              onupdate=tzware_datetime),
                    sa.Column('bar', sa.String(128), index=True))


def downgrade():
    op.drop_table('foos')
