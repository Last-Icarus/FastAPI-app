from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import Depends, HTTPException, status
from ..database import get_db



def show_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def show_blog(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'There is no blog with ID of {id}')
    return blog

def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title = request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'detail:': f'The post with ID of {id} was deleted'}

def update(id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no blog with ID of {id}')
    blog.update({'title': request.title,'body':request.body})
    db.commit()
    return 'Updated succesfully'

