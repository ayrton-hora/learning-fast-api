from os import stat
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel, validator

app = FastAPI()

class PostDTO(BaseModel):
    tittle: str
    content: str
    published: bool = True
    rating: Optional[int] = None

    @validator("tittle", "content")
    def check_strings(cls, v):
        assert len(v) > 0, "Empty strings are not allowed!"
        return v

class UpdatePostDTO(BaseModel):
    tittle = ""
    content = ""
    published: bool = True,
    rating: Optional[int] = None

my_posts = [
    { "tittle": "tittle 1", "content": "content 1", "published": True, "rating": None, "id": 0 }, 
    { "tittle": "tittle 2", "content": "content 2", "published": True, "rating": None, "id": 1 }, 
    { "tittle": "tittle 3", "content": "content 3", "published": True, "rating": None, "id": 2 }]

@app.get("/")
def root():
    return { "message": "Welcome to my API" }

# @app.get("/posts")
# def get_posts():
#     return {"data": my_posts}

@app.get("/posts")
def get_posts(id: int | None = None):
    if id is not None:
        try:
            return { "data": my_posts[id] }

        except:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id: '{id}' was not found.")

    else:
        return { "data": my_posts }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post_dto: PostDTO):
    new_post = post_dto.dict()
    new_post["id"] = len(my_posts)
    my_posts.append(new_post)
    return { "data": new_post }

@app.patch("/posts")
def update_post(post_dto: UpdatePostDTO, id: int | None = None):
    if id is not None:
        try:
            print(post_dto.published)
            target_post = my_posts[id]
            target_post["tittle"] = post_dto.tittle if post_dto.tittle != "" else  target_post["tittle"]
            target_post["content"] = post_dto.content if post_dto.content != "" else target_post["content"]
            target_post["published"] = post_dto.published
            target_post["rating"] = post_dto.rating if post_dto.rating != None else  target_post["rating"]
            return target_post

        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: '{id}' does not exist")
    else:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"The 'id' field is required.")

@app.delete("/posts")
def delete_post(id: int | None = None):
    if id is not None:
        try:
            my_posts.pop(id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id: '{id}' does not exist.")
