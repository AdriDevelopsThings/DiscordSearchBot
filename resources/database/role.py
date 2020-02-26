from typing import List

from sqlalchemy import Column, Text, and_, Integer
from .. import Session, db


class Role(db):
    __tablename__ = "admin_roles"
    id = Column(Integer, primary_key=True)
    admin_role_id = Column(Text, nullable=False)
    guild_id = Column(Text, nullable=False)

    def __init__(self, guild_id: str, admin_role_id: str):
        self.admin_role_id = admin_role_id
        self.guild_id = guild_id


def get_roles(guild, s=None) -> List[Role]:
    session: Session = Session() if s is None else s
    roles = session.query(Role).filter(Role.guild_id == guild.id).all()
    if s is None:
        session.close()
    return roles


def add_role(guild, admin_role, s=None):
    session: Session = Session() if s is None else s
    session.add(Role(guild.id, admin_role.id))
    session.commit()
    if s is None:
        session.close()


def remove_role(guild, admin_role, s=None):
    session: Session = Session() if s is None else s
    role = session.query(Role).filter(and_(Role.admin_role_id == admin_role.id, Role.guild_id == guild.id)).first()
    session.delete(role)
    session.commit()
    if s is None:
        session.close()
