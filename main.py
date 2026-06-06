from routers.user import router as user_router
from routers.auth import router as auth_router
from routers.todo import router as todo_router
from fastapi import FastAPI
from database.db import create_table
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title = "Todo app",
    version = "0.0.1",
    description = "connecting to database"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],         #in this we need to put the domains about how many domains we want to allow or if we want to allow all domains then we can put *
    allow_methods = ["*"],        # how many methods we wanna allow like "Put", "Get"
    allow_headers = ["*"],         # headers like "x-auth" or any
    allow_credentials = True
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(todo_router)


@app.on_event("startup") ## Runs when the FastAPI app starts
def on_startup():
    create_table()