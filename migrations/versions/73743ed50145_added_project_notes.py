"""added project notes

Revision ID: 73743ed50145
Revises: 
Create Date: 2019-10-31 23:04:16.999368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73743ed50145'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('notes', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('projects', 'notes')
    # ### end Alembic commands ###