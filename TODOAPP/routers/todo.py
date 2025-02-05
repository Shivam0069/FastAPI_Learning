from fastapi import Depends, HTTPException, Path, APIRouter
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(tags=["todo"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


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


@router.get("/todos", status_code=status.HTTP_200_OK)
def read_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Todos).filter(user.get("id") == Todos.owner_id).all()


@router.get("/todos/completed", status_code=status.HTTP_200_OK)
def completed_todos(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    completed_todos = (
        db.query(Todos)
        .filter(Todos.owner_id == user.get("id"), Todos.completed == True)
        .all()
    )
    if completed_todos is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return completed_todos


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(
    db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_item = (
        db.query(Todos)
        .filter(Todos.owner_id == user["id"], Todos.id == todo_id)
        .first()
    )

    if todo_item is not None:
        return todo_item
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, user: user_dependency, todo: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = Todos(**todo.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()
    return None


@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo_by_id(
    db: db_dependency,
    user: user_dependency,
    todo: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.owner_id == user["id"], Todos.id == todo_id)
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        todo_model.title = todo.title
        todo_model.description = todo.description
        todo_model.priority = todo.priority
        todo_model.completed = todo.completed
        db.commit()
    return None


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(
    db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo = (
        db.query(Todos)
        .filter(Todos.owner_id == user.get("id"), Todos.id == todo_id)
        .first()
    )
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    else:
        db.delete(todo)
        db.commit()
    return None
