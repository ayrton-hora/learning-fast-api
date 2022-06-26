from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status

from ..database import db
from .. import models, schemas

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(id: int | None = None, database: Session = Depends(db)):
    if id is not None:
        try:
            data = database.query(models.Post).filter(models.Post.id == id).first()

            if data != None:
                return [data]

            else:
                raise HTTPException(status.HTTP_404_NOT_FOUND, 
                    detail=f"Post with id: '{id}' was not found.")

        except:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id: '{id}' was not found.")

    else:
        data = database.query(models.Post).all()
        return data

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post_dto: schemas.CreatePost, database: Session = Depends(db)):
    new_post = models.Post(**post_dto.dict())
    database.add(new_post)
    database.commit()
    database.refresh(new_post)
    return new_post

@router.patch("/", response_model=schemas.PostResponse)
def update_post(post_dto: schemas.UpdatePost, id: int | None = None, database: Session = Depends(db)):
    if id is not None:
        data = database.query(models.Post).filter(models.Post.id == id)

        if data.first() != None:
            if post_dto.title != "":
                data.update({ "title": post_dto.title }, synchronize_session=False)

            if post_dto.content != "":
               data.update({ "content": post_dto.content }, synchronize_session=False)

            data.update({ "published": post_dto.published }, synchronize_session=False)

            database.commit()
            return data.first()

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id: '{id}' does not exist")

    else:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"The 'id' field is required.")

@router.delete("/")
def delete_post(id: int | None = None, database: Session = Depends(db)):
    if id is not None:
        data = database.query(models.Post).filter(models.Post.id == id).first()

        if data != None:
            database.delete(data)
            database.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
                detail=f"Post with id: '{id}' does not exist.")
    
    else:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail=f"The 'id' field is required.")