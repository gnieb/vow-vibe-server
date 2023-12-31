"""add wedding_date column to Weddings table

Revision ID: 658bcc3d8442
Revises: 0a324b13ac98
Create Date: 2023-11-03 11:46:03.395091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '658bcc3d8442'
down_revision = '0a324b13ac98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weddings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wedding_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('weddings', schema=None) as batch_op:
        batch_op.drop_column('wedding_date')

    # ### end Alembic commands ###
