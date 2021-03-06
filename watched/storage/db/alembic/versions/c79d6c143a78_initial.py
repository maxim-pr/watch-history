"""Initial

Revision ID: c79d6c143a78
Revises: 
Create Date: 2022-04-02 13:52:48.296624

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c79d6c143a78'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type', postgresql.ENUM('film', 'show', name='media_type'), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__media'))
    )
    op.create_table('reviews',
    sa.Column('media_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.SmallInteger(), nullable=True),
    sa.Column('review', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['media_id'], ['media.id'], name=op.f('fk__reviews__media_id__media'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('media_id', name=op.f('pk__reviews'))
    )
    op.create_table('watch_history',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('media_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['media_id'], ['media.id'], name=op.f('fk__watch_history__media_id__media'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__watch_history'))
    )
    op.create_index(op.f('ix__user_id'), 'watch_history', ['user_id'], unique=False)
    op.create_table('watch_history_shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('season', sa.SmallInteger(), nullable=True),
    sa.Column('ep1', sa.SmallInteger(), nullable=True),
    sa.Column('ep2', sa.SmallInteger(), nullable=True),
    sa.Column('finished_season', sa.Boolean(), nullable=True),
    sa.Column('finished_show', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['watch_history.id'], name=op.f('fk__watch_history_shows__id__watch_history'), onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk__watch_history_shows'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('watch_history_shows')
    op.drop_index(op.f('ix__user_id'), table_name='watch_history')
    op.drop_table('watch_history')
    op.drop_table('reviews')
    op.drop_table('media')
    # ### end Alembic commands ###
