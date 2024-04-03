from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from config import SECRET_KEY

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd.verify(plain_password, hashed_password)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
    
def verify_token_not_exception(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: int = payload.get("sub")
        if user_name is None:
            return
        return user_name
    except JWTError:
        return