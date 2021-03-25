"""empty message

Revision ID: dde37bd2d0f1
Revises: 952a91da6b81
Create Date: 2018-09-06 15:55:19.423951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dde37bd2d0f1'
down_revision = '952a91da6b81'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('quantity', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'quantity')
    # ### end Alembic commands ###