import time
from fastapi import FastAPI
from . import models
import psycopg2
from psycopg2.extras import RealDictCursor
from .database import engine
from .routers import post, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

my_posts = [
    {
        "id": 1,
        "title": "Post 1 title",
        "content": "Post 1 Content",
    },
    {
        "id": 2,
        "title": "Favourite Cars",
        "content": "I prefer Toyota Crown",
    },
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Welcome to my APIs"}

