from configargparse import ArgumentParser, YAMLConfigFileParser
from configargparse import Namespace


ENV_VAR_PREFIX = 'WATCHED_'


def setup_args_parser() -> ArgumentParser:
    parser = ArgumentParser(
        auto_env_var_prefix=ENV_VAR_PREFIX,
        default_config_files=['config.yml'],
        config_file_parser_class=YAMLConfigFileParser,
        args_for_setting_config_path=['-c', '--config-file'],
        config_arg_help_message='Config file path',
    )

    api_group = parser.add_argument_group('API')
    api_group.add_argument('--api-host', default='0.0.0.0')
    api_group.add_argument('--api-port', type=int, default=8080)

    db_group = parser.add_argument_group('Database')
    db_group.add_argument('--db-user', default='postgres')
    db_group.add_argument('--db-password', default='postgres')
    db_group.add_argument('--db-host', default='localhost')
    db_group.add_argument('--db-port', type=int, default=5432)
    db_group.add_argument('--db-name', default='watched')

    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])

    return parser


def parse_args() -> Namespace:
    parser = setup_args_parser()
    args = parser.parse_args()
    args.db_url = get_db_url(args)
    return args


def get_db_url(args: Namespace) -> str:
    db_url = 'postgresql+asyncpg://{}:{}@{}:{}/{}'
    db_url = db_url.format(args.db_user, args.db_password,
                           args.db_host, args.db_port, args.db_name)
    return db_url
