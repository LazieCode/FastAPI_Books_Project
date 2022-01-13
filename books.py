from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

Books = {
    'book_1': {'title': 'Title_one', 'author': 'Author_one'},
    'book_2': {'title': 'Title_two', 'author': 'Author_two'},
    'book_3': {'title': 'Title_three', 'author': 'Author_three'},
    'book_4': {'title': 'Title_four', 'author': 'Author_four'},
    'book_5': {'title': 'Title_five', 'author': 'Author_five'},
}

class DirectionName(str, Enum):  
    north = "North"
    south = "South"
    west = "West"
    east = "East"

@app.get('/direction/{direction_name}')
async def get_direction(direction_name: DirectionName): # Now this is for enumerating path parameter.... Enumerating basically means that except the names mentioned in the class the user cannot write anything other than that.
    if direction_name.north == direction_name:
        return "North"
    
    if direction_name.south == direction_name:
        return "South"
    
    if direction_name.east == direction_name:
        return "East"
    
    return "West"

@app.get('/')
async def read_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books = Books.copy()
        del new_books[skip_book]
        return new_books
    else:
        return Books

@app.post('/') # This is used to create a new book  
async def create_book(book_title, book_author):
    curr_book_id = len(Books) + 1
    Books[f'book_{curr_book_id}'] = {'title': book_title, 'author': book_author}
    return Books

@app.put('/{book_name}') # This is used to update a book or create a new one if the old book is not present.
async def update_book(book_name, book_title, book_author):
    Books[book_name] = {'title': book_title, 'author': book_author}
    return Books

@app.delete('/{book_name}') # Deleting a book
async def delete_book(book_name):
    del Books[book_name]
    return f'{book_name} is deleted'

@app.get('/book/{book_id}')
async def read_book_title(book_id:int): # Type Casting done with the help of pydantics.
    return {'Book_id': book_id}

@app.get('/books/{title}')
async def read_book_title(title):
    for book in Books.values():
        if(book['title'] == title):
            return book
        
    return {'Message': 'Book not found'}




        