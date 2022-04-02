from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, SmallInteger, Text, DateTime, Boolean
)
from sqlalchemy.dialects.postgresql import ENUM

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
    Column('user_id', Integer, nullable=False, index=True),
    Column('datetime', DateTime, nullable=False),
    Column('media_id', Integer, ForeignKey('media.id', ondelete='CASCADE',
                                           onupdate='CASCADE'))
)


watch_history_shows_table = Table(
    'watch_history_shows',
    metadata,
    Column('id', Integer, ForeignKey('watch_history.id', ondelete='CASCADE',
                                     onupdate='CASCADE'), primary_key=True),
    Column('season', SmallInteger),
    Column('ep1', SmallInteger),
    Column('ep2', SmallInteger),
    Column('finished_season', Boolean),
    Column('finished_show', Boolean, nullable=False)
)


media_table = Table(
    'media',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('type', ENUM('film', 'show', name='media_type'), nullable=False),
    Column('name', Text, nullable=False)
)


reviews_table = Table(
    'reviews',
    metadata,
    Column('media_id', Integer, ForeignKey('media.id', ondelete='CASCADE',
                                           onupdate='CASCADE'),
           primary_key=True),
    Column('score', SmallInteger),
    Column('review', Text)
)
