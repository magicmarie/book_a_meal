"""empty message

Revision ID: e751a66f07c2
Revises: b6fa43ed328f
Create Date: 2018-08-21 12:55:17.253560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e751a66f07c2'
down_revision = 'b6fa43ed328f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('menus', sa.Column('menu_name', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('menus', 'menu_name')
    # ### end Alembic commands ###
