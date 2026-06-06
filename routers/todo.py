from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path, status, APIRouter
from sqlmodel import select
from model.todo import Todo
from database.db import SessionDependency, create_table
from request_model.TodoRequest import TodoRequest
from response_model.TodoResponse import TodoResponse
from utility import validate_token

router = APIRouter(
    prefix= "/todo",
    tags= ["Todo"]
)

auth_user_dependency = Annotated[dict, Depends(validate_token)]

## To create todo

@router.post("/create", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todoReq:TodoRequest, session: SessionDependency, user:auth_user_dependency):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    todo_data = todoReq.model_dump()
    todo_data['user_id'] = user.get("id")
    todo =  Todo.model_validate(todo_data)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


#To fetch Todo

@router.get("/all", response_model=list[TodoResponse])
async def get_todo(session:SessionDependency, user:auth_user_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not Authorized")
    query = select(Todo).where(Todo.user_id == user.get("id"))
    result = session.exec(query).all()
    return result



#To get todo by it

@router.get("/{todo_id}", response_model = TodoResponse)
async def get_todo_by_id(session: SessionDependency, user:auth_user_dependency ,todo_id:int=Path(ge=1)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user.get("id"))).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo



#To get Todo by priority

@router.get("/by_priority/{priority}", response_model = list[TodoResponse])
async def get_todo_by_priority(session:SessionDependency, user: auth_user_dependency,priority:int=Path(le=5, ge=1)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    query = select(Todo).where(Todo.priority==priority, Todo.user_id == user.get("id"))
    todo = session.exec(query).all()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo



#To update the Todo by id

@router.put("/update/{todo_id}", response_model = TodoResponse)
async def get_update_todo(session:SessionDependency, user:auth_user_dependency,  todoReq: TodoRequest, todo_id:int = Path(ge=1)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id == user.get("id"))).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Todo not Found")
    
    todo.title = todoReq.title
    todo.description = todoReq.description
    todo.priority = todoReq.priority
    todo.is_completed = todoReq.is_completed

    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo




#To delete todo by id

@router.delete("/delete/{todo_id}")
async def delete_todo_by_id(session:SessionDependency, user: auth_user_dependency,todo_id:int = Path(ge=1)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized")
    todo = session.exec(select(Todo).where(Todo.id == todo_id, Todo.user_id ==user.get("id"))).first()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return