from alembic.config import CommandLine

from .alembic_config import setup_alembic_config


def main():
    alembic = CommandLine()
    alembic.parser.add_argument('--db-url', required=True, help='Database URL')
    alembic_args = alembic.parser.parse_args()

    if 'cmd' not in alembic_args:
        alembic.parser.error('too few arguments')
        exit(128)
    else:
        config = setup_alembic_config(alembic_args)
        exit(alembic.run_cmd(config, alembic_args))


if __name__ == '__main__':
    main()
