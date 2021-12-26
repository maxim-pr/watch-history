from sqlalchemy import MetaData, Table, Column, Integer, Text

metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('username', Text, nullable=False, unique=True),
    Column('first_name', Text),
    Column('last_name', Text),
    Column('password', Text, nullable=False)
)
