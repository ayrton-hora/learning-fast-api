from datetime import datetime
from turtle import title
from pydantic import BaseModel, EmailStr, validator

from app.models import User

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(Post):
    @validator("title", "content")
    def check_strings(cls, v):
        assert len(v) > 0, "Empty strings are not allowed!"
        return v

class UpdatePost(BaseModel):
    title = ""
    content = ""
    published: bool = True

class PostResponse(BaseModel):
    id: int
    title: str
    published: bool

    class Config:
        orm_mode = True

class User(BaseModel):
    email: EmailStr
    password: str

class CreateUser(User):
    @validator("email", "password")
    def check_empty(cls, v):
        assert len(v) > 0, "Empty strings are not allowed!"
        return v

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
