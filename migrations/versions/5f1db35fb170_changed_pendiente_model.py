"""changed pendiente model

Revision ID: 5f1db35fb170
Revises: 46c676d7c6a9
Create Date: 2021-06-18 17:26:16.790029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f1db35fb170'
down_revision = '46c676d7c6a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pendiente', sa.Column('priority', sa.Integer(), nullable=True))
    op.drop_column('pendiente', 'due_date')
    op.drop_column('pendiente', 'title')
    op.drop_column('pendiente', 'prior')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pendiente', sa.Column('prior', sa.INTEGER(), nullable=True))
    op.add_column('pendiente', sa.Column('title', sa.VARCHAR(length=100), nullable=True))
    op.add_column('pendiente', sa.Column('due_date', sa.DATETIME(), nullable=True))
    op.drop_column('pendiente', 'priority')
    # ### end Alembic commands ###
