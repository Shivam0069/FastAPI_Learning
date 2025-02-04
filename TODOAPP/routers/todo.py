from fastapi import Depends, HTTPException, Path, APIRouter
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field


router = APIRouter(tags=["todo"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str = Field(
        title="Title of the todo",
        description="Title of the todo",
        min_length=3,
        max_length=50,
    )
    description: str = Field(
        title="Description of the todo",
        description="Description of the todo",
        min_length=3,
        max_length=100,
    )
    priority: int = Field(
        title="Priority of the todo",
        description="Priority of the todo",
        ge=1,
        le=5,
    )
    completed: bool = Field(
        title="Status of the todo", description="Status of the todo"
    )


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todos_list = db.query(Todos).filter(Todos.id == todo_id).first()
    print(todos_list)
    if todos_list is not None:
        return todos_list
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, todo: TodoRequest):
    todo_model = Todos(**todo.model_dump())
    db.add(todo_model)
    db.commit()


@router.put("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def update_todo_by_id(db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.completed = todo.completed
        db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo)
        db.commit()
