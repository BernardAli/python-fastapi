import time
import os

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgresql = os.environ.get("DDTYPE")
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")
postgresserver = os.environ.get("SERVER")
db = os.environ.get("DBNAME")


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f"{postgresql}://{user}:{password}@{postgresserver}/{db}"
# SQLALCHEMY_DATABASE_URL = "postgresql://allgift:Matt6:33@localhost/new-fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='new-fastapi', user='allgift', password='Matt6:33',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to the database failed")
        print(f"Error {error}")
        time.sleep(2)
