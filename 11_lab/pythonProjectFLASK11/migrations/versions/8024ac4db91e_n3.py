"""n3

Revision ID: 8024ac4db91e
Revises: 
Create Date: 2023-12-19 19:29:57.228526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8024ac4db91e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('content', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('content')
        batch_op.drop_column('title')

    # ### end Alembic commands ###
