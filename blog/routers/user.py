from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends, status, HTTPException

from blog.routers.blog import delete_blog
from .. import schemas,models
from ..database import get_db
from passlib.context import CryptContext
from ..repository import user



router = APIRouter()
router = APIRouter(
    prefix='/user',
    tags=['Users']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request,db)

@router.get('/', response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(get_db)):
    return user.show_all(db)

@router.get('/{id}',  status_code=200,response_model=schemas.ShowUser)
def show_user(id,db: Session = Depends(get_db)):
    return user.show_user(id,db)

