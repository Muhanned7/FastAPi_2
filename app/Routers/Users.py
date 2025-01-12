from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  engine, get_db
from .. import models, schemas, utils
from typing import Optional, List

router = APIRouter(
    prefix="/Users",
    tags = ["Users"]
)



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Ret_user)
def create_user(user:schemas.user,db:Session =Depends(get_db)):
    new_user= models.User(**user.dict())
    hashed_password = utils.hash(user.password)
    new_user.password = hashed_password
    try:
        db.add(new_user)

        db.commit()
    except Exception as e:
        print("cannot create User:", e)
    db.refresh(new_user)

    return new_user


@router.get("/",status_code=status.HTTP_201_CREATED, response_model=List[schemas.Ret_user] )
def get_users(db:Session=Depends(get_db)):
    user =db.query(models.User).all()
    if not user :
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                            detail=f"Not able to get Users")
    
    return user

@router.get("/{id}",status_code=status.HTTP_201_CREATED, response_model=schemas.Ret_user )
def get_users(id:int, db:Session=Depends(get_db)):
    user =db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, 
                            detail=f"User with {id} does not exist")
    
    return user


    
