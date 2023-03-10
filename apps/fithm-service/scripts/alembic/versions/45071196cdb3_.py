"""empty message

Revision ID: 45071196cdb3
Revises: 4582c84fe985
Create Date: 2022-06-30 15:48:56.283832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45071196cdb3'
down_revision = '4582c84fe985'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('account_positions_portfolio_id_fkey', 'account_positions', type_='foreignkey')
    op.drop_column('account_positions', 'account_number')
    op.drop_column('account_positions', 'portfolio_id')
    op.drop_column('account_positions', 'broker_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account_positions', sa.Column('broker_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('account_positions', sa.Column('portfolio_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('account_positions', sa.Column('account_number', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('account_positions_portfolio_id_fkey', 'account_positions', 'portfolios', ['portfolio_id'], ['id'])
    # ### end Alembic commands ###
