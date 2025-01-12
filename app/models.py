from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
     __tablename__ = "Posts"


     id = Column(Integer, primary_key=True, nullable=False)
     Title = Column(String, nullable=-False)
     Content=Column(String, nullable=False)
     published = Column(String, server_default='TRUE',nullable=False)
     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
     owner_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
     owner = relationship("User")
     phone_number = Column(String)



class User(Base):
     __tablename__ = "Users"
     id =Column(Integer,primary_key=True, nullable=False)
     email=Column(String, nullable=False, unique=True)
     password = Column(String,nullable=False)
     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
     __tablename__ = "Votes"
     post_id=Column(Integer, ForeignKey("Posts.id",ondelete="CASCADE"),nullable=False, primary_key=True)
     user_id = Column(Integer, ForeignKey("Users.id",ondelete="CASCADE"),nullable=False, primary_key=True)


