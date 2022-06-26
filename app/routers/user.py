from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from ..database import db
from .. import models, schemas, utils

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(id: int | None = None, database: Session = Depends(db)):
    if id is not None:
        try:
            data = database.query(models.User).filter(models.User.id == id).first()

            if data != None:
                return [data]

            else:
                raise HTTPException(status.HTTP_404_NOT_FOUND, 
                    detail=f"User with id: '{id}' was not found.")

        except:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
                detail=f"User with id: '{id}' was not found.")

    else:
        data = database.query(models.User).all()
        return data

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user_dto: schemas.CreateUser, database: Session = Depends(db)):
    hashed_password = utils.hash(user_dto.password)
    user_dto.password = hashed_password
    new_user = models.User(**user_dto.dict())
    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    return new_user
