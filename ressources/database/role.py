from sqlalchemy import Column, Text, and_, Integer, BigInteger
from .. import Session, db


class Role(db):
    __tablename__ = "admin_roles"
    admin_role_id = Column(Integer, primary_key=True)
    role_id = Column(Text, nullable=False)
    guild_id = Column(Text, nullable=False)

    def __init__(self, guild_id: str, admin_role_id: str):
        self.admin_role_id = admin_role_id
        self.guild_id = guild_id


def get_roles(guild_id: str, s=None):
    session: Session = Session() if s is None else s
    servers = session.query(Role).filter(Role.guild_id == guild_id).all()
    if s is None:
        session.close()
    return servers


def add_role(guild_id: str, admin_role_id: str, s=None):
    session: Session = Session() if s is None else s
    role = Role(guild_id, admin_role_id)
    session.add(role)
    session.commit()
    if s is None:
        session.close()


def remove_role(guild_id: str, s=None):
    session: Session = Session() if s is None else s
    session.remove(get_roles(guild_id, session))
    session.commit()
    if s is None:
        session.close()


def update_role(guild_id: str, admin_role_id: str, update_content, s=None):
    session: Session = Session() if s is None else s
    session.query(Role).filter(
        and_(Role.guild_id == guild_id, Role.admin_role_id == admin_role_id)
    ).update(update_content)
    session.commit()
    if s is None:
        session.close()
