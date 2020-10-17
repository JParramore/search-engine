"""Change position in Word to be an integer

Revision ID: 50825c5124cc
Revises: 76fd231f76bc
Create Date: 2020-10-17 17:05:52.224709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50825c5124cc'
down_revision = '76fd231f76bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.alter_column('position',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('location', schema=None) as batch_op:
        batch_op.alter_column('position',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    # ### end Alembic commands ###