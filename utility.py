
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from passlib.context import CryptContext
from database.db import SessionDependency
from model.user import User
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

## To store the password in encrypted form

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

## To validate password - its a inbuilt function

def validate_password(hashed_password:str, password:str) -> bool:
    return pwd_context.verify(hash=hashed_password, secret=password)

async def check_user_credentials(email:str, password:str, session:SessionDependency):
    # Read and get user by email
    user = session.exec(select(User).where(User.email == email)).first()
    
    if not user:
    # if user is not available return false
        return False
    # validate user password with haspassword, if not validate then return false
    if not validate_password(user.password, password):
        return False
    # if email and password are validate then return user
    return user

async def create_jwt_token(data:dict, expiry_time:timedelta):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expiry_time
    to_encode.update({"exp": expire})

    access_token = jwt.encode(claims=to_encode, algorithm=JWT_ALGORITHM, key=JWT_SECRET)  ##converting data into JWT tokens

    return {
    "access_token": access_token,
    "token_type": "bearer"
}




def decode_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")



oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
async def validate_token(token: Annotated[str, Depends(oauth2_bearer)]):
    payload = decode_token(token)

    subject = payload.get("sub")

    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to authorize")
    return payload
