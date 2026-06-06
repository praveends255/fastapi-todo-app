from datetime import datetime
from sqlmodel import Field
from model.UserBase import UserBase
from request_model.UserRequest import UserRequest


class User(UserRequest, table= True):
    id: int|None =Field(primary_key=True, default=None)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    