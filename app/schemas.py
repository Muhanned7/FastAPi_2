from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import Field
from typing_extensions import Annotated


class Post(BaseModel):
    Title:str
    Content:str
    published:bool =True




class CreatePost(Post):
    pass

class Ret_user(BaseModel):
    id:int
    email:EmailStr
    class Config:
        orm_mode =True

class PostRet(Post):
    id:int
    created_at: datetime
    owner_id: int
    owner : Ret_user
    class Config:
        orm_mode =True

class PostVote(BaseModel):
    Post:PostRet
    Votes:int
    class Config:
        orm_mode =True



class user(BaseModel):
    email:EmailStr
    password:str



class Token(BaseModel):
    access_token : str
    token_type:str

class TokenData(BaseModel):
    id: Optional[int]

class Vote(BaseModel):
    post_id:int 
    dir:Annotated[int, Field(strict=True, le=1)]


