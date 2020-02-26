from os import environ
from typing import Optional

config_object: Optional["Config"] = None


def get_config() -> "Config":
    return config_object


class Config:
    BOT_TOKEN: str = ""
    GOOGLE_API_TOKEN: str = ""
    GOOGLE_CX_ALL: str = ""
    GOOGLE_CX_STACKOVERFLOW: str = ""
    config_file: str = ""
    db_host: str = ""
    db_port: str = ""
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    ctx_types = ["google", "stackoverflow"]
    message_reacting_expire = 5 # in days
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
        self.GOOGLE_CX_ALL = environ.get("GOOGLE_CX_ALL")
        if not self.GOOGLE_CX_ALL:
            print("GOOGLE_CX_ALL not correctly provided! Exiting!")
            exit(1)
        self.GOOGLE_CX_STACKOVERFLOW = environ.get("GOOGLE_CX_STACKOVERFLOW")
        if not self.GOOGLE_CX_STACKOVERFLOW:
            print("GOOGLE_CX_STACKOVERFLOW not correctly provided! Exiting!")
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

        self.SQLALCHEMY_DATABASE_URI = (
            "mysql+pymysql://"
            + self.db_user
            + ":"
            + self.db_password
            + "@"
            + self.db_host
            + ":"
            + self.db_port
            + "/"
            + self.db_name
            + "?charset=utf8"
        )


def load():
    global config_object
    config_object = Config()
