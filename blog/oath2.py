from fastapi import Depends
from . import token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(login_token = Depends(oauth2_scheme)):
    return token.verify_token(login_token)