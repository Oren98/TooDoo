from loguru import logger

logger.remove(0)
logger.add(
    "logs\\log_{time}.log", rotation="100 MB", format="{time} | {level} | {message}"
)
