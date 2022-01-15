from fastapi import FastAPI, status, HTTPException, Depends # standds for dependencies
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):

    title: str
    description: Optional[str] =  Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6, description="Priority should be between 1 to 5")
    complete: bool  


@app.get("/")
async def read_all(db: Session = Depends(get_db)): # Now the execution of this function depends on the execution of the get_db function so that is why we have used depends 
    return db.query(models.Todos).all()


@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise ItemNotFoundException()


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return succesful_response(201)


@app.put("/{todo_id}")
async def update_todo(todo_id:int, todo: Todo, db: Session = Depends(get_db)):

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is None:
        raise ItemNotFoundException()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return succesful_response(200)


@app.delete('/{todo_id}')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    
    if todo_model is None:
        raise ItemNotFoundException()

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

    db.commit()

    return succesful_response(200)


def succesful_response(status_code: int):
    return{
        'status': status_code,
        'message': 'Successful'
    }

def ItemNotFoundException():
    return HTTPException(status_code=404, detail="Item not found")