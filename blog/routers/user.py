from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends, status, HTTPException
from .. import schemas,models
from ..database import get_db
from passlib.context import CryptContext


router = APIRouter()


def bcrypt(element: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(element)

@router.post('/user',tags=['Users'],status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return request

@router.get('/user', tags=['Users'],response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/user/{id}', tags=['Users'], status_code=200,response_model=schemas.ShowUser)
def show_user(id,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'There is no user with ID of {id}')
    return user