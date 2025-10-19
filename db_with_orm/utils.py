from passlib.context import CryptContext
# using argon2 for hashing passwords
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)