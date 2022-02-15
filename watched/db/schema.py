from sqlalchemy import (
    MetaData, Table, Index, Column, ForeignKey,
    Integer, SmallInteger, Text, DateTime
)


metadata = MetaData()

watched_table = Table(
    'watched',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text, nullable=False),
    Column('datetime', DateTime, nullable=False),
    Column('user_id', Integer, nullable=False),
    Column('score', SmallInteger),
    Column('review', Text)
)

Index('ix__user_id_datetime',
      watched_table.c.user_id,
      watched_table.c.datetime)

Index('ix__user_id_score',
      watched_table.c.user_id,
      watched_table.c.score)


watched_shows_table = Table(
    'watched_shows',
    metadata,
    Column('watched_id', ForeignKey('watched.id', ondelete='CASCADE')),
    Column('season', SmallInteger),
    Column('first_episode', SmallInteger),
    Column('last_episode', SmallInteger),
)
