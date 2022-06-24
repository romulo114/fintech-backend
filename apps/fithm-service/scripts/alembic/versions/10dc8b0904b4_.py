"""empty message

Revision ID: 10dc8b0904b4
Revises: 43abb1894c41
Create Date: 2022-06-24 00:42:20.096677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10dc8b0904b4'
down_revision = '43abb1894c41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account_position_price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_position_id', sa.Integer(), nullable=False),
    sa.Column('business_price_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_position_id'], ['account_positions.id'], ),
    sa.ForeignKeyConstraint(['business_price_id'], ['business_price.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('model_position_price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_position_id', sa.Integer(), nullable=False),
    sa.Column('business_price_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_price_id'], ['business_price.id'], ),
    sa.ForeignKeyConstraint(['model_position_id'], ['model_positions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('accounts', sa.Column('account_position_price_id', sa.Integer(), nullable=True))
    op.create_foreign_key("cash_position_price", 'accounts', 'account_position_price', ['account_position_price_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("cash_position_price", 'accounts', type_='foreignkey')
    op.drop_column('accounts', 'account_position_price_id')
    op.drop_table('model_position_price')
    op.drop_table('account_position_price')
    # ### end Alembic commands ###