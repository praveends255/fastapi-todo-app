from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    email:str = Field(unique=True, nullable=False)
    name: str = Field(nullable=False, min_length=3, max_length=20)