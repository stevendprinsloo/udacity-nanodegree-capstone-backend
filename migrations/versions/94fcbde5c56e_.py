"""empty message

Revision ID: 94fcbde5c56e
Revises: fe089b059acf
Create Date: 2022-05-16 18:51:53.840616

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94fcbde5c56e'
down_revision = 'fe089b059acf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('castings', 'actor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('castings', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('castings', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('castings', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.alter_column('castings', 'movie_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('castings', 'actor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
