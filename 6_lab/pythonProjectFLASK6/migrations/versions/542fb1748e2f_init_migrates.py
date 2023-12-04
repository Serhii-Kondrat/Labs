"""init migrates

Revision ID: 542fb1748e2f
Revises: 
Create Date: 2023-12-01 17:26:27.165159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '542fb1748e2f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('password')

    # ### end Alembic commands ###
