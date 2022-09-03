from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from .. import schemas,models
from ..database import get_db
from ..hashing import Hash
 
def create(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return request

def show_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

def show_user(id,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'There is no user with ID of {id}')
    return user