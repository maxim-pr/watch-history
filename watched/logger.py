import logging


def setup_logger(log_level: str):
    logger = logging.getLogger(__package__)
    logger.setLevel(log_level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    formatter = logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
