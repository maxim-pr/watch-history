import logging

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)
file_handler = logging.FileHandler('watched.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s'
)

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
