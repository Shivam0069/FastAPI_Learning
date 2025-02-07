from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from .auth import get_current_user
from sqlalchemy.orm import Session
from typing import Annotated
from ..models import Todos
from ..database import SessionLocal

router = APIRouter(tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/admin/todo", status_code=status.HTTP_200_OK)
def get_all_todos(db: db_dependency, user: user_dependency):
    print(user)
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todos = db.query(Todos).all()
    return {"todos": todos}


@router.delete("/admin/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_by_id(
    db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)
):
    if user is None or user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
