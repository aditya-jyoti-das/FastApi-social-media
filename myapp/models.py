from .database import Base
from sqlalchemy import Column, Integer, String, Boolean , ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship





class Posts(Base):
    __tablename__='Posts'

    id= Column(Integer, primary_key=True, nullable=False)
    title=Column(String(1000), nullable=False)
    content=Column(String(1000),nullable=False)
    published=Column(Boolean, server_default= text('True') , default=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    owner=relationship('User')

class User(Base):
    __tablename__='users'
    
    id=Column(Integer, primary_key=True, nullable=False)
    email=Column(String(100), nullable =False ,unique=True)
    password=Column(String(100),nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))



class Vote(Base):
    __tablename__="votes"

    user_id= Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),primary_key=True)
    post_id= Column(Integer,ForeignKey("Posts.id",ondelete='CASCADE'),primary_key=True)



