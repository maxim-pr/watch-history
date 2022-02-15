from sqlalchemy import MetaData, Table, Index, Column, ForeignKey, Integer, Text, DateTime


metadata = MetaData()

films_table = Table(
    'films',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Text, nullable=False)
)

films_users_table = Table(
    'films__users',
    metadata,
    Column('film_id', ForeignKey('films.id', ondelete='CASCADE')),
    Column('user_id', Integer, nullable=False),
    Column('watched_at', DateTime, nullable=False)
)

Index('ix__user_id_datetime', films_users_table.c.user_id, films_users_table.c.datetime)