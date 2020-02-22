from os import environ
from typing import Optional
from json import load as load_js, JSONDecodeError, dump as dump_js
config_object: Optional["Config"] = None


def get_config() -> "Config":
    return config_object


class Config:
    prefixes: dict = {}
    role_settings: dict = {}
    BOT_TOKEN: str = ""
    GOOGLE_API_TOKEN: str = ""
    config_file: str = ""
    json_config: dict = {}
    db_host: str = ""
    db_port: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    SQLALCHEMY_DATABASE_URI: str = ""

    def __init__(self):
        self.BOT_TOKEN = environ.get("BOT_TOKEN")
        if not self.BOT_TOKEN:
            print("BOT_TOKEN not correctly provided! Exiting!")
            exit(1)
        self.GOOGLE_API_TOKEN = environ.get("GOOGLE_API_TOKEN")
        if not self.GOOGLE_API_TOKEN:
            print("GOOGLE_API_TOKEN not correctly provided! Exiting!")
            exit(1)
        self.config_file = environ.get("CONFIG_FILE")
        if not self.GOOGLE_API_TOKEN:
            print("GOOGLE_API_TOKEN not correctly provided! Exiting!")
            exit(1)

        # database
        self.db_host = environ.get("DB_HOST")
        self.db_port = environ.get("DB_PORT")
        self.db_user = environ.get("DB_USER")
        self.db_password = environ.get("DB_PASSWORD")
        self.db_name = environ.get("DB_NAME")

        for i in [self.db_name, self.db_port, self.db_host, self.db_password, self.db_user]:
            if not i:
                print("Database configuration not complete! Exiting")
                exit(1)

        self.SQLALCHEMY_DATABASE_URI = \
            "mysql+pymysql://" + self.db_user + ":" + self.db_password \
            + "@" + self.db_host + ":" + self.db_port \
            + "/" + self.db_name + "?charset=utf8"

    def load_file(self, exit_if_exception: bool = False) -> bool:
        json: dict = {}
        try:
            with open(self.config_file, "r") as f:
                json = load_js(f)
        except FileNotFoundError:
            if exit_if_exception:
                print("CONFIG_FILE does not exist! Exiting!")
                exit(1)
            print(f"Can not reload config, because {self.config_file} does not exist!")
        except JSONDecodeError:
            if exit_if_exception:
                print("CONFIG_FILE does not contain valid json! Exiting!")
                exit(1)
            print(f"Can not reload config, because {self.config_file} does not contain valid json!")
        self.json_config = json
        return True

    def load_config_from_file(self, exit_if_exception: bool = False) -> None:
        if self.load_file(exit_if_exception):
            try:
                self.prefixes = self.json_config["prefixes"]
            except KeyError:
                if exit_if_exception:
                    print("CONFIG_FILE does not contain list of prefixes! Exiting!")
                    exit(1)
                print(f"Can not reload prefixes, because {self.config_file} does not contain list of prefixes!")
            try:
                self.role_settings = self.json_config["roles"]
            except KeyError:
                if exit_if_exception:
                    print("CONFIG_FILE does not contain list of roles! Exiting!")
                    exit(1)
                print(f"Can not reload roles, because {self.config_file} does not contain list of roles!")

    def save_to_json(self):
        self.json_config.update({"roles": self.role_settings, "prefixes": self.prefixes})
        with open(self.config_file, "w") as f:
            dump_js(self.json_config, f)

    def add_guild(self, guild):
        self.prefixes.update({guild.id: "§"})
        self.role_settings.update({guild.id: []})
        self.save_to_json()


def load():
    global config_object
    config_object = Config()
    config_object.load_config_from_file(exit_if_exception=True)
