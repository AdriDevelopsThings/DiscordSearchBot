from sqlalchemy import Column, Text, Integer, String
from sqlalchemy.orm.exc import NoResultFound

from .. import Session, db


class ServerNotFound(BaseException):
    pass


class Server(db):
    __tablename__ = "servers"
    server_id = Column(Integer, nullable=False, primary_key=True)
    guild_id = Column(Text, nullable=False)
    prefix = Column(String(10), nullable=False, default="§")
    google_reaction = Column(Text, nullable=True)

    def __init__(self, guild_id, google_reaction="", prefix="§"):
        self.guild_id = guild_id
        self.prefix = prefix
        self.google_reaction = google_reaction


def get_server(guild, s=None):
    server = None
    session: Session = Session(expire_on_commit=False) if s is None else s
    try:
        server = session.query(Server).filter(Server.guild_id == guild.id).one()
    except NoResultFound:
        server = initiliaze_server(guild, session)
    finally:
        if s is None:
            session.close()
    return server


def initiliaze_server(guild, s=None):
    session: Session = Session() if s is None else s
    server = Server(guild.id)
    session.add(server)
    session.commit()
    if s is None:
        session.close()
    print(f"{guild} has been initialiazed")
    return server


def leave_server(guild, s=None):
    session: Session = Session() if s is None else s
    session.delete(get_server(guild.id, session))
    session.commit()
    if s is None:
        session.close()


def update_prefix(guild, prefix: str):
    session = Session()
    get_server(guild, session).prefix = prefix
    session.commit()
    session.close()


def update_google_reaction(guild, emoji):
    session = Session()
    get_server(guild, session).google_reaction = str(emoji.id)
    session.commit()
    session.close()
