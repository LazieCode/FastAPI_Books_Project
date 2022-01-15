from sqlalchemy import Boolean, Column, Integer, String
from database import Base

#Creating a todos table

class Todos(Base):
    __tablename__ = "TodoList"  # actual table name

    # Now defining the columns for the table. id, title, description, priority, status

    id = Column(Integer, primary_key = True, index = True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)


