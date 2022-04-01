import logging


def setup_logger(logger: logging.Logger, log_level: str):
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
