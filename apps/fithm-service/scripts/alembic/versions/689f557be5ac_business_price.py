"""Add business price table, remove price table, remover refernces to price table

Revision ID: 689f557be5ac
Revises: cdc4a7130d06
Create Date: 2022-06-24 00:03:30.410589

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '689f557be5ac'
down_revision = 'cdc4a7130d06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('business_price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('business_id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id', 'symbol', name='business_security_price')
    )
    op.drop_table('prices')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('prices',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('account_position_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('model_position_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('trade_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('symbol', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['account_position_id'], ['account_positions.id'], name='prices_account_position_id_fkey'),
    sa.ForeignKeyConstraint(['model_position_id'], ['model_positions.id'], name='prices_model_position_id_fkey'),
    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], name='prices_trade_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='prices_pkey')
    )
    op.drop_table('business_price')
    # ### end Alembic commands ###
