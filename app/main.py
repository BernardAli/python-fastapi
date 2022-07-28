import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic.main import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
    return {"data": my_posts}


@app.post("/posts")
def new_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = random.randrange(10e10)
    print(post.dict())
    my_posts.append(post_dict)
    return {"new_post": post_dict}


@app.get("/posts/{id}")
def get_posts(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post with {id} does not exist"}
    # print(post)
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def get_posts(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}