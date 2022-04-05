from configparser import ConfigParser
from dataclasses import dataclass

GENERAL_SECTION = 'general'
API_SECTION = 'api'
DB_SECTION = 'db'
REDIS_SECTION = 'redis'


@dataclass
class APIConfig:
    host: str
    port: int


@dataclass
class DBConfig:
    user: str
    password: str
    host: str
    port: int
    name: str
    log_sql: bool

    def __post_init__(self):
        self.url = f'postgresql+asyncpg://' \
                   f'{self.user}:{self.password}@' \
                   f'{self.host}:{self.port}/{self.name}'


@dataclass
class RedisConfig:
    user: str
    password: str
    host: str
    port: str
    db: int

    def __post_init__(self):
        self.url = f'redis://{self.user}:{self.password}@' \
                   f'{self.host}:{self.port}/{self.db}'


@dataclass
class Config:
    api: APIConfig
    db: DBConfig
    redis: RedisConfig
    log_level: str


def read_config() -> Config:
    config_parser = ConfigParser()
    config_parser.read('config.ini')

    api_config = APIConfig(
        host=config_parser.get(API_SECTION, 'host'),
        port=config_parser.getint(API_SECTION, 'port')
    )
    db_config = DBConfig(
        user=config_parser.get(DB_SECTION, 'user'),
        password=config_parser.get(DB_SECTION, 'password'),
        host=config_parser.get(DB_SECTION, 'host'),
        port=config_parser.getint(DB_SECTION, 'port'),
        name=config_parser.get(DB_SECTION, 'name'),
        log_sql=config_parser.getboolean(DB_SECTION, 'log_sql')
    )
    redis_config = RedisConfig(
        user=config_parser.get(REDIS_SECTION, 'user'),
        password=config_parser.get(REDIS_SECTION, 'password'),
        host=config_parser.get(REDIS_SECTION, 'host'),
        port=config_parser.getint(REDIS_SECTION, 'port'),
        db=config_parser.getint(REDIS_SECTION, 'db')
    )
    log_level = config_parser.get(GENERAL_SECTION, 'log_level')
    return Config(api_config, db_config, redis_config, log_level)
