from fastapi import Depends
import blog.token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(login_token = Depends(oauth2_scheme)):
    return blog.token.verify_token(login_token)