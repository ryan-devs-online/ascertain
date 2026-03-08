import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db.base import Base

load_dotenv()
database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url, echo=True)


def start_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session
