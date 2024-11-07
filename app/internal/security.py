from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "62dba6d8567eacee1484951b47fed0417359bac650266452d65cb0453417dfc2"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(claims: dict):
    return jwt.encode(claims, key=SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
