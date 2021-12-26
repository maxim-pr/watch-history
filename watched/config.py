from dataclasses import dataclass

from environs import Env


@dataclass
class ApiConfig:
    host: str
    port: int


@dataclass
class DbConfig:
    host: str
    port: int
    user: str
    password: str
    name: str


@dataclass
class Config:
    api: ApiConfig
    db: DbConfig
    log_level: str


def read_config() -> Config:
    env = Env()
    env.read_env()

    with env.prefixed('WATCHED_'):
        with env.prefixed('API_'):
            api_host = env.str('HOST')
            api_port = env.int('PORT')

        with env.prefixed('DB_'):
            db_host = env.str('HOST')
            db_port = env.int('PORT')
            db_user = env.str('USER')
            db_password = env.str('PASSWORD')
            db_name = env.str('NAME')

        log_level = env.str('LOG_LEVEL')

    api_config = ApiConfig(api_host, api_port)
    db_config = DbConfig(db_host, db_port, db_user, db_password, db_name)
    config = Config(api_config, db_config, log_level)

    return config


def get_db_url(db_config: DbConfig):
    return f'postgresql+asyncpg://{db_config.user}:{db_config.password}@' \
           f'{db_config.host}:{db_config.port}/{db_config.name}'
