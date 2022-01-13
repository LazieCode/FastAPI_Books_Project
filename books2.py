from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()

class Book(BaseModel): # This is how we create a class using the base model and now we will be able to create instances of a class basically objects which we can directally pass as request. 
    id: UUID
    title: str
    author: str
    description: str
    rating: int

Books = []

@app.get('/')
async def read_all_books():
    return Books

@app.post("/")
async def create_book(book: Book):
    Books.append(book)
    return Books,book




