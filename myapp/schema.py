# Dependency

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional,List
from pydantic.types import conint
from pydantic import Field
from typing_extensions import Annotated
class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class userOut(BaseModel):
    created_at:datetime
    id: int 
    email: EmailStr
    class Config:
        
        from_attributes = True


class CreatePost(PostBase):
    pass


class Posts(PostBase):
    id: int
    created_at: datetime
    owner_id:int
    owner: userOut
    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Posts:Posts
    votes:int
    
class UserBase(BaseModel):
    email:EmailStr
    password:str


class updateUser(UserBase):
    pass

class createUser(UserBase):
    pass



class Userlogin(BaseModel):
    email:EmailStr
    password: str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]=None 


class Vote(BaseModel):
    post_id:int 
    dir:  Annotated[int, Field(strict=True, le=1)]

