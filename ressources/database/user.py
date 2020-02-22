from sqlalchemy import Column, Text, and_, Integer
from .. import Session, db


class User(db):
    __tablename__ = "banned_users"
    ban_id = Column(Integer, primary_key=True)
    user_id = Column(Text, nullable=False)
    guild_id = Column(Text, nullable=False)

    def __init__(self, user_id: str, guild_id: str):
        self.user_id = user_id
        self.guild_id = guild_id


def get_user(user_id: str, guild_id: str):
    session = Session()
    user_list = session.query(User).filter(and_(User.user_id==user_id, User.guild_id==guild_id)).all()
    session.close()
    return user_list


def add_user(user_id: str, guild_id: str):
    if len(get_user(user_id, guild_id)) == 0:
        session = Session()
        session.add(User(user_id, guild_id))
        session.commit()
        session.close()


def remove_user(user_id: str, guild_id: str):
    user_list = get_user(user_id, guild_id)
    if len(user_list) > 0:
        session = Session()
        session.delete(user_list[0])
        session.commit()
        session.close()
        return True
    return False
