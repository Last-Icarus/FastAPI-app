from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get('/')
def show():
    return {'data': 'blog list'}

@app.get('/blog')
def blogs(limit: int = 50,published: bool = True, sort:Optional[str]=None):
    if published:
        return {'data': f'There are {limit} published blogs'}
    else:
        return {'data': f'There are {limit} blogs'}

@app.get('blog/unpublished')
def unpub():
    return {'data':'nodata'}

@app.get('/blog/{id}')
def blog(id: int):
    return {"blog id:":id}

@app.get('/blog/{id}/comments')
def comments(id: int):
    return {f"comments №{id}:":'test'}

class Blog(BaseModel):
    title: str
    text: str
    author: str
    tegs: Optional[str] = None
    

@app.post('/blog')
def create_blog(request: Blog):
    return {'Title':request.title, 'text':request.text, 'author':request.author}

