from datetime import timedelta
from typing import Annotated
from fastapi import Depends, FastAPI, APIRouter, status, HTTPException
from sqlmodel import select
from model.user import User
from database.db import SessionDependency
from request_model.UserRequest import UserRequest
from response_model.UserResponse import UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from utility import check_user_credentials, create_jwt_token, hash_password



router = APIRouter(
    prefix= "/auth",
    tags= ["Auth"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(session:SessionDependency, new_user: UserRequest):
    user = User.model_validate(new_user)
    email_e = session.exec(select(User).where(User.email == new_user.email)).first()
    if email_e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already register")
    
    user.password = hash_password(user.password) ## To make the password encrypted
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/login")
async def user_login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],session:SessionDependency):
    email = form_data.username
    password = form_data.password

    #validate credentials - email and password

    user = await check_user_credentials(email, password, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong Password or email")
    
    #Creating JWT Token

    data = {
        'sub': user.email,
        'id': user.id,
        'name': user.name
    }
    
    token_dict = await create_jwt_token(data, timedelta(minutes=15))
    return token_dict