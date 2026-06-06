from contextlib import contextmanager
from typing import Annotated

from dotenv import load_dotenv
import os
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

load_dotenv()

DB_HOST = os.getenv("MYSQLHOST")
DB_PORT = os.getenv("MYSQLPORT")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")

DB_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DB_URL, echo=True)

def create_table():
    SQLModel.metadata.create_all(engine)



@contextmanager
def get_session_context():
    session = Session(engine)

    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_session():
    with get_session_context() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_session)]