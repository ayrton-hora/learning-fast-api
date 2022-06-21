from pydantic import BaseModel, validator

class PostDTO(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePostDTO(PostDTO):
    @validator("title", "content")
    def check_strings(cls, v):
        assert len(v) > 0, "Empty strings are not allowed!"
        return v

class UpdatePostDTO(BaseModel):
    title = ""
    content = ""
    published: bool = True

class PostResponse(PostDTO):
    id: int

    class Config:
        orm_mode = True
