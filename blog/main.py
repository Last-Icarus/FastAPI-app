from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
from . import schemas, models
from .database import SessionLocal, engine 
from sqlalchemy.orm import Session
from passlib.context import CryptContext



app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def bcrypt(element: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(element)

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog,db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.post('/user',status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return request



@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'detail:': f'The post with ID of {id} was deleted'}

@app.put('/blog/{id}')
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'There is no blog with ID of {id}')
    blog.update(request).update({'title':'updated title'})
    db.commit()
    return 'Updated succesfully'




@app.get('/blog',response_model=List[schemas.ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200,response_model=schemas.ShowBlog)
def show(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'There is no blog with ID of {id}')
    return blog

@app.get('/user',response_model=List[schemas.ShowUser])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users