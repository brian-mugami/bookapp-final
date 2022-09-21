"""final db change

Revision ID: 868e7c6ae760
Revises: 4af2964f208a
Create Date: 2022-09-21 13:55:28.745140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '868e7c6ae760'
down_revision = '4af2964f208a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'read')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('read', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
