from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from starlette.responses import JSONResponse


class NegativeNumberException(Exception): # custom exceptions
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()

class Book(BaseModel): # This is how we create a class using the base model and now we will be able to create instances of a class basically objects which we can directally pass as request. 
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(title = "Description of Book", max_length=100, min_length=1)
    rating: int = Field(gt= -1, lt=101)

    class Config: # Config is a predefined class, another class name wont work and same is the case with schema_extra. 
        schema_extra = {
            "example": {
                "id": "155947d9-a591-4ecf-b988-10753e8dd6ec",
                "title": "CSE",
                "author": "Shourya K Chirania",
                "description": "Nice Book",
                "rating": 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(max_length=50)
    description: Optional[str] = Field(None, title = "description of the book", max_length=100)

    class Config:
        schema_extra = {
            "example": {
                "id": "155947d9-a591-4ecf-b988-10753e8dd6ec",
                "title": "CSE",
                "author": "Shourya K Chirania",
                "description": "Nice Book" 
            }
        }

Books = []


@app.exception_handler(NegativeNumberException)
async def negative_no_exception(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={"message" : 'Books cannot be negative.'})


@app.post("/books/login")
async def login(username: str = Form(...), password: str = Form(...)): #if we dont mention the str to be of type form then fastapi will think that it is a query parameter.
    return {"username": username, "password": password}

@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"Randon-Header": random_header}


@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):

    if(books_to_return and books_to_return< 0):
        raise NegativeNumberException(books_to_return=books_to_return)

    if(len(Books)< 1):
        create_books_noapi()
    
    if(books_to_return and len(Books) >= books_to_return > 0):
        i = 0
        new_books = []
        while(i< books_to_return):
            new_books.append(Books[i])
            i += 1
            
        return new_books

    return Books

@app.get("/book/{book_id}")
async def read_book_uuid(book_id: UUID):
    for book in Books:
        if(book.id == book_id):
            return book
        
    raise itemNotFoundException

@app.get("/book/rating/{book_id}", response_model=BookNoRating) # What the response model does is it returns a response based on the model class which we have passsed as the parameter and FastAPI automatically converts the current model into the response model.
async def read_book_noRating(book_id: UUID):
    for book in Books:
        if(book.id == book_id):
            return book
        
    raise itemNotFoundException


@app.post("/", status_code=status.HTTP_201_CREATED) # so status code 200 means that the process was succesful but status code 201 means that something was succesfully created.
async def create_book(book: Book):
    Books.append(book)
    return Books

@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in Books:
        counter += 1
        if(x.id == book_id):
            Books[counter - 1] = book
            return Books[counter - 1]

    raise itemNotFoundException

@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0

    for x in Books:
        counter += 1
        if(x.id == book_id):
            del Books[counter - 1]
            return Books

    raise itemNotFoundException
            

def create_books_noapi():
    book_1 = Book(id="855947d9-a591-4ecf-b988-10753e8dd6ec",
                  title="Title1", author = "Author_1", 
                  description= "Description_1",
                  rating = "60")
    book_2 = Book(id="855947d9-a592-4ecf-b988-20753e8dd6ec",
                  title="Title2", author = "Author_2", 
                  description= "Description_2",
                  rating = "70")
    book_3 = Book(id="855947d9-a593-4ecf-b988-30753e8dd6ec",
                  title="Title3", author = "Author_3", 
                  description= "Description_3",
                  rating = "80")

    Books.append(book_1)
    Books.append(book_2)
    Books.append(book_3)


# Making exceptions 

def itemNotFoundException():
    return HTTPException(status_code=404, detail="Item not found", headers={"X-Header-Error": "Nothing seen at the UUID"})



