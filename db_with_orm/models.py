from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from database import Base

class Chat(Base):
    __tablename__ = "chats_orm"

    id = Column(Integer, primary_key=True, nullable=False)
    query = Column(String, nullable=False)
    response = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text(("now()")))
    owner_id = Column(Integer, ForeignKey("users_orm.id", ondelete="CASCADE"), nullable=False)

class User(Base):
    __tablename__ = "users_orm"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text(("now()")))
