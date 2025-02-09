from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from starlette import status
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="TodoApp/templates")

router = APIRouter(tags=["todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


### Pages ###


@router.get("/todos/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

        return templates.TemplateResponse(
            "todo.html", {"request": request, "todos": todos, "user": user}
        )

    except:
        return redirect_to_login()


@router.get("/todos/add-todo-page")
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(
            "add-todo.html", {"request": request, "user": user}
        )

    except:
        return redirect_to_login()


@router.get("/todos/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse(
            "edit-todo.html", {"request": request, "todo": todo, "user": user}
        )

    except:
        return redirect_to_login()


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
