from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my APIs"}

