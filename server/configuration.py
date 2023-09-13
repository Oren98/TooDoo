from tomllib import load

from consts import CONFIG_FILE_PATH, CONFIG_OPEN_MODE


class Configuration(object):
    def __init__(self, config: dict) -> None:
        self.results_per_query = config["database"]["results_per_query"]
        self.database_url = config["database"]["database_url"]
        self.users_table_name = config["database_tables"]["users_table_name"]
        self.todos_table_name = config["database_tables"]["todos_table_name"]
        self.userstodosrelations_table_name = config["database_tables"][
            "userstodosrelations_table_name"
        ]
        self.log_file_path = config["logger"]["log_file_path"]
        self.log_rotation_size = config["logger"]["log_rotation_size"]
        self.log_format = config["logger"]["log_format"]


with open(CONFIG_FILE_PATH, CONFIG_OPEN_MODE) as config_file:
    configuration = Configuration(load(config_file))
