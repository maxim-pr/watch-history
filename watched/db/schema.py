from sqlalchemy import (
    MetaData, Table, Index, Column, ForeignKey,
    Integer, SmallInteger, Text, DateTime, Boolean
)

naming_convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': (
        'fk__%(table_name)s__' 
        '%(all_column_names)s__' 
        '%(referred_table_name)s'
    ),
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=naming_convention)


watch_history_table = Table(
    'watch_history',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, nullable=False),
    Column('datetime', DateTime, nullable=False),
    Column('is_show', Boolean, nullable=False)
)

Index('ix__user_id', watch_history_table.c.user_id)


watch_history_films_table = Table(
    'watch_history_films',
    metadata,
    Column('id', Integer,
           ForeignKey('watch_history.id', ondelete='CASCADE', onupdate='CASCADE'),
           primary_key=True),
    Column('film_name', Text, nullable=False)
)


watch_history_shows_table = Table(
    'watch_history_shows',
    metadata,
    Column('id', Integer,
           ForeignKey('watch_history.id', ondelete='CASCADE', onupdate='CASCADE'),
           primary_key=True),
    Column('show_id', Integer,
           ForeignKey('shows.id', ondelete='CASCADE', onupdate='CASCADE'),
           nullable=False),
    Column('first_episode', SmallInteger),
    Column('last_episode', SmallInteger),
    Column('season', SmallInteger),
    Column('finished_season', Boolean),
    Column('finished_show', Boolean)
)


shows_table = Table(
    'shows',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, nullable=False),
    Column('name', Text, nullable=False)
)


watched_table = Table(
    'watched',
    metadata,
    Column('id', Integer,
           ForeignKey('watch_history.id', ondelete='CASCADE', onupdate='CASCADE'),
           primary_key=True),
    Column('score', SmallInteger),
    Column('review', Text)
)
