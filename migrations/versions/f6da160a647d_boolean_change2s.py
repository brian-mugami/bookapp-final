"""boolean change2s

Revision ID: f6da160a647d
Revises: d6f6e09d23e7
Create Date: 2022-08-17 21:46:39.114420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6da160a647d'
down_revision = 'd6f6e09d23e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('book_pic', sa.String(), nullable=True),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('date_added', sa.DateTime(timezone=True), nullable=True),
    sa.Column('read', sa.Integer(), nullable=False),
    sa.Column('about', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
