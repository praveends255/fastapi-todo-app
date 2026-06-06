from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from database.db import SessionDependency
from model.user import User
from request_model.PasswordChangeRequest import PasswordChangeRequest
from utility import hash_password, validate_password, validate_token

router = APIRouter(
    prefix="/user",
    tags= ["user"]
)

auth_user_dependency = Annotated[dict, Depends(validate_token)]

@router.put("/change_password")
async def change_password(user_password: PasswordChangeRequest, session: SessionDependency, user:auth_user_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    #Read user by user id
    db_user = session.exec(select(User).where(User.id == user.get("id"))).first()
    #check db.password == user_password.current_passowrd
    db_password = db_user.password
    is_same = validate_password(hashed_password=db_password, password = user_password.current_password)
    if is_same:
        db_user.password = hash_password(user_password.new_password)
        session.add(db_user)
        session.commit()
        return {"message : Password changed"}
    # if true update new password
    # if false, return 400
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Current password is wrong")