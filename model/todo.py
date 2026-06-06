from datetime import datetime
from sqlmodel import SQLModel, Field
from model.TodoBase import TodoBase

class Todo(TodoBase, table=True):
    id:int | None = Field(primary_key=True, default=None)
    created_at: datetime =Field(nullable=False, default=datetime.now())
    user_id : int | None = Field(foreign_key="user.id") 