import random
import time
from fastapi import FastAPI, Response, status, HTTPException
from pydantic.main import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/")
def root():
    return {"message": "Welcome to my APIs"}


@app.get("/posts")
def all_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def new_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get("/posts/{id}")
def get_posts(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id), ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post with {id} does not exist"}
    # print(post)
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    posts = cursor.fetchone()
    conn.commit()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    return {"data": posts}
