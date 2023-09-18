from loguru import logger

from configuration import configuration

logger.remove(0)
logger.add(
    configuration.log_file_path,
    rotation=configuration.log_rotation_size,
    format=configuration.log_format,
)
