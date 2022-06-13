import os, time
import psycopg2

from typing import Optional
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, validator
from fastapi import Body, FastAPI, HTTPException, Response, status

class PostDTO(BaseModel):
    title: str
    content: str
    published: bool = True

    @validator("title", "content")
    def check_strings(cls, v):
        assert len(v) > 0, "Empty strings are not allowed!"
        return v

class UpdatePostDTO(BaseModel):
    title = ""
    content = ""
    published: bool = True

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"], 
            database=os.environ["POSTGRES_DATABASE"], 
            user=os.environ["POSTGRES_USER"], 
            password=os.environ["POSTGRES_PASSWORD"],
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(">>> Connection established with database.")
        break

    except Exception as err:
        print(">>> Failed to connect to database.")
        print(f"--> Error: {err}")
        time.sleep(2)

@app.get("/health")
def root():
    return { "message": "Welcome to my API, I'm alive!" }

@app.get("/posts")
def get_posts(id: int | None = None):
    if id is not None:
        try:
            cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id)))
            records = cursor.fetchone()
            if records != None:
                return { "data": records }

            else:
                raise HTTPException(status.HTTP_404_NOT_FOUND, 
                    detail=f"Post with id: '{id}' was not found.")

        except:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id: '{id}' was not found.")

    else:
        cursor.execute("SELECT * FROM posts")
        records = cursor.fetchall()
        return { "data": records }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post_dto: PostDTO):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post_dto.title, post_dto.content, post_dto.published))
    new_post = cursor.fetchone()
    conn.commit()
    return { "data": new_post }

@app.patch("/posts")
def update_post(post_dto: UpdatePostDTO, id: int | None = None):
    if id is not None:
        try:
            if post_dto.title != "":
                cursor.execute("UPDATE posts SET title = %s WHERE id = %s RETURNING *", (post_dto.title, str(id)))
            
            if post_dto.content != "":
                cursor.execute("UPDATE posts SET content = %s WHERE id = %s RETURNING *", (post_dto.content, str(id)))
            
            cursor.execute("UPDATE posts SET published = %s WHERE id = %s RETURNING *", (post_dto.published, str(id)))

            records = cursor.fetchmany()

            conn.commit()

            return { "data": records}

        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: '{id}' does not exist")
    else:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"The 'id' field is required.")

@app.delete("/posts")
def delete_post(id: int | None = None):
    if id is not None:
        try:
            cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id)))
            cursor.fetchone()
            conn.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        except:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id: '{id}' does not exist.")
    
    else:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"The 'id' field is required.")

