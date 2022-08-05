"""picture adjustment

Revision ID: 3501c005c035
Revises: 2b846f750f65
Create Date: 2022-08-01 10:20:10.026260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3501c005c035'
down_revision = '2b846f750f65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('book_pic', sa.String(), nullable=True))
    op.add_column('suggestions', sa.Column('book_pic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('suggestions', 'book_pic')
    op.drop_column('books', 'book_pic')
    # ### end Alembic commands ###