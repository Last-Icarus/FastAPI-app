from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(element: str):
        return pwd_context.hash(element)

    def verify(hashed_password,plain_password):
        return pwd_context.verify(plain_password,hashed_password)