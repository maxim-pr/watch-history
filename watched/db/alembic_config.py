import os
from argparse import Namespace
from pathlib import Path

from alembic.config import Config

CURR_DIR = Path(__file__).parent.resolve()
ALEMBIC_INI_PATH = CURR_DIR.joinpath('alembic.ini')
ALEMBIC_DIR_PATH = CURR_DIR.joinpath('alembic')


def setup_alembic_config(alembic_args: Namespace) -> Config:
    if not os.path.isabs(alembic_args.config):
        alembic_args.config = str(ALEMBIC_INI_PATH)

    alembic_config = Config(file_=alembic_args.config,
                            ini_section=alembic_args.name,
                            cmd_opts=alembic_args)

    if not os.path.isabs(alembic_config.get_main_option('script_location')):
        alembic_config.set_main_option(
            'script_location', str(ALEMBIC_DIR_PATH)
        )
    alembic_config.set_main_option('sqlalchemy.url', alembic_args.db_url)

    return alembic_config
