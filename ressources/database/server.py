from sqlalchemy import Column, Text, and_, Integer, String, BigInteger
from sqlalchemy.orm.exc import NoResultFound

from .. import Session, db


class ServerNotFound(BaseException):
    pass


class Server(db):
    __tablename__ = "servers"
    server_id = Column(Integer, nullable=False, primary_key=True)
    guild_id = Column(Text, nullable=False)
    prefix = Column(String, nullable=False, default="§")
    google_reaction = Column(Text, nullable=True)

    def __init__(self, guild_id, prefix="§"):
        self.guild_id = guild_id
        self.prefix = prefix


def get_server(guild_id: str, s=None):
    try:
        session: Session = Session() if s is None else s
        server = session.query(Server).filter(Server.guild_id == guild_id).one()
        if s is None:
            session.close()
        return server
    except NoResultFound:
        raise ServerNotFound()


def join_server(guild_id: str, s=None):
    session: Session = Session() if s is None else s
    server = Server(guild_id)
    session.add(server)
    session.commit()
    if s is None:
        session.close()
    return server


def leave_server(guild_id: str, s=None):
    session: Session = Session() if s is None else s
    session.remove(get_server(guild_id, session))
    session.commit()
    if s is None:
        session.close()


def update_server(guild_id: str, update_content, s=None):
    session: Session = Session() if s is None else s
    session.query(Server).filter(Server.guild_id == guild_id).update(update_content)
    session.commit()
    if s is None:
        session.close()
