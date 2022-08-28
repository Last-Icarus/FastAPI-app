from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends, status, HTTPException
from .. import schemas,models
from ..database import get_db


router = APIRouter()


@router.get('/blog',tags=['Blogs'],response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog',tags=['Blogs'], status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog,db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}',tags=['Blogs'],status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'detail:': f'The post with ID of {id} was deleted'}

@router.put('/blog/{id}',tags=['Blogs'])
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no blog with ID of {id}')
    blog.update(request).update({'title':'updated title'})
    db.commit()
    return 'Updated succesfully'



@router.get('/blog/{id}',tags=['Blogs'], status_code=200,response_model=schemas.ShowBlog)
def show_blog(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'There is no blog with ID of {id}')
    return blog
    