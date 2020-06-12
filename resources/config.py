from os import environ
from typing import Optional
from resources.core.evironment import Environment, Version

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
    ctx_types = ["google", "stackoverflow", "wikipedia", "lmgtfy", "youtube"]
    version = Version()
    environment = Environment()
    github_link = "https://github.com/AdriBloober/DiscordSearchBot"
    message_reacting_expire = 5 # in days
    authors = "AdriBloober#9372 & TNT2k#7587"
    SQLALCHEMY_DATABASE_URI: str = ""
    LOG_GUILD = None
    LOG_CHANNEL = None

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
        self.GOOGLE_CX_WIKIPEDIA = environ.get("GOOGLE_CX_WIKIPEDIA")
        if not self.GOOGLE_CX_WIKIPEDIA:
            print("GOOGLE_CX_WIKIPEDIA not correctly provided! Exiting!")
            exit(1)
        self.GOOGLE_CX_YOUTUBE = environ.get("GOOGLE_CX_YOUTUBE")
        if not self.GOOGLE_CX_YOUTUBE:
            print("GOOGLE_CX_YOUTUBE not correctly provided! Exiting!")
            exit(1)
        self.LOG_GUILD = environ.get("LOG_GUILD")
        self.LOG_CHANNEL = environ.get("LOG_CHANNEL")

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
