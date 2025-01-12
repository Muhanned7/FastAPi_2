from passlib.context import CryptContext



pwd_concept = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password:str):
    return pwd_concept.hash(password)

def verify(password:str, hashed_password:str):
    return pwd_concept.verify(password,hashed_password)
