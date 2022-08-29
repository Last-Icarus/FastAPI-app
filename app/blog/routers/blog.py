from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends, status, HTTPException

from .. import schemas,models, oath2
from ..database import get_db
from ..repository import blog



router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/',response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.show_all(db)

@router.get('/{id}', status_code=200,response_model=schemas.ShowBlog)
def show_blog(id,db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.show_blog(id,db)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog,db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.create(request, db)


@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.delete(id,db)

@router.put('/{id}',tags=['Blogs'])
def update_blog(id:int, request: schemas.Blog, db: Session = Depends(get_db),get_current_user: schemas.User = Depends(oath2.get_current_user)):
    return blog.update(id,request,db)


