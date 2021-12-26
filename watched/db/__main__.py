from argparse import Namespace
from pathlib import Path

from alembic.config import CommandLine, Config as AlembicConfig

from ..config import read_config, get_db_url

CURR_DIR = Path(__file__).parent
ALEMBIC_INI_PATH = CURR_DIR.joinpath('alembic.ini')
ALEMBIC_DIR_PATH = CURR_DIR.joinpath('alembic')


def setup_alembic_config(alembic_args: Namespace) -> AlembicConfig:
    # alembic.ini file
    if not Path(alembic_args.config).is_absolute():
        alembic_args.config = str(ALEMBIC_INI_PATH)

    alembic_config = AlembicConfig(file_=alembic_args.config,
                                   ini_section=alembic_args.name,
                                   cmd_opts=alembic_args)

    # alembic directory
    if not Path(alembic_config.get_main_option(
            'script_location')).is_absolute():
        alembic_config.set_main_option('script_location',
                                       str(ALEMBIC_DIR_PATH))

    alembic_config.set_main_option('sqlalchemy.url', alembic_args.db_url)
    return alembic_config


def main():
    alembic = CommandLine()
    config = read_config()
    config_db_url = get_db_url(config.db)
    alembic.parser.add_argument(
        '--db-url',
        default=config_db_url,
        help='Database URL'
    )

    alembic_args = alembic.parser.parse_args()

    if 'cmd' not in alembic_args:
        alembic.parser.error('too few arguments')
        exit(128)

    alembic_config = setup_alembic_config(alembic_args)
    exit(alembic.run_cmd(alembic_config, alembic_args))
