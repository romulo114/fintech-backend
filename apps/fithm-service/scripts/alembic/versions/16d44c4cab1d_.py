"""empty message

Revision ID: 16d44c4cab1d
Revises: 45071196cdb3
Create Date: 2022-06-30 16:22:47.478838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16d44c4cab1d'
down_revision = '45071196cdb3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account_positions', sa.Column('active', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account_positions', 'active')
    # ### end Alembic commands ###