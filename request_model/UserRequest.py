

from sqlmodel import Field
from model.UserBase import UserBase


class UserRequest(UserBase):
    password:str = Field(max_length=250, nullable=False)