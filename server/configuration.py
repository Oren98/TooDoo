from tomllib import load

from consts import CONFIG_FILE_PATH, CONFIG_OPEN_MODE
from exceptions import ConfigurationError


class Configuration(object):
    def __init__(self, config: dict) -> None:
        self.results_per_query: int = config["database"]["results_per_query"]
        self.database_url: str = config["database"]["database_url"]
        self.users_table_name: str = config["database_tables"]["users_table_name"]
        self.todos_table_name: str = config["database_tables"]["todos_table_name"]
        self.userstodosrelations_table_name: str = config["database_tables"][
            "userstodosrelations_table_name"
        ]
        self.log_file_path: str = config["logger"]["log_file_path"]
        self.log_rotation_size: str = config["logger"]["log_rotation_size"]
        self.log_format: str = config["logger"]["log_format"]


def is_empty(field_name: str, value: int | str):
    """
    given a key value pair, will check if the value is empty (None or by type)

    :param field_name: the key, if its empty will raise an exception with the given key
    :param value: value to check
    :raises ConfigurationError: raise if None
    :raises ConfigurationError: raise if empty string ""
    :raises ConfigurationError: raise if empty list []
    """
    if value is None:
        raise ConfigurationError(f"{field_name} is None")
    if (type(value) is str) and (value == ""):
        raise ConfigurationError(f'{field_name} is an empty string ""')
    if (type(value) is list) and (value == []):
        raise ConfigurationError(f"{field_name} is an empty list []")


def validate_config(config: Configuration):
    """
    validate if the configuration is ok

    :param config: the given configuration
    :raises ConfigurationError: is the problem with the configuration
    """
    for key, value in config.__dict__.items():
        is_empty(key, value)
    if config.results_per_query <= 0:
        raise ConfigurationError("result_per_quuery sould be greater then 0")


with open(CONFIG_FILE_PATH, CONFIG_OPEN_MODE) as config_file:
    configuration = Configuration(load(config_file))
    validate_config(configuration)
