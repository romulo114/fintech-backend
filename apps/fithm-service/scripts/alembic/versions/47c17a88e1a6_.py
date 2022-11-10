"""empty message

Revision ID: 47c17a88e1a6
Revises: fb388767bb32
Create Date: 2022-10-30 19:51:26.393754

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import column

# revision identifiers, used by Alembic.
revision = '47c17a88e1a6'
down_revision = 'fb388767bb32'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.alter_column('business_price', 'price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=False)
    op.create_check_constraint("ck_price_greater_zero", "business_price", column('price') > 0)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('business_price', 'price',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               nullable=True)
    op.drop_constraint("ck_price_greater_zero", "business_price")
    # ### end Alembic commands ###
