from configparser import ConfigParser
from dataclasses import dataclass


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


@dataclass
class Config:
    api: APIConfig
    db: DBConfig
    log_level: str


def read_config() -> Config:
    config_parser = ConfigParser()
    config_parser.read("config.ini")

    api_config = APIConfig(**config_parser['api'])
    db_config = DBConfig(**config_parser['db'])
    log_level = config_parser['general']['log_level']

    return Config(api_config, db_config, log_level)
