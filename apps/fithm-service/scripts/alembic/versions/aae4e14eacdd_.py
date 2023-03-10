"""empty message

Revision ID: aae4e14eacdd
Revises: 0896c83a6a8c
Create Date: 2022-06-10 00:28:04.233262

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aae4e14eacdd'
down_revision = '0896c83a6a8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trades', sa.Column('status', postgresql.ENUM('active', 'inactive', 'retired', name='trade_status'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trades', 'status')
    # ### end Alembic commands ###
