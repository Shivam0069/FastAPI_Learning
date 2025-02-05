from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(tags=["user"])


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/user/profile", status_code=status.HTTP_200_OK)
def get_profile(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    return {"user_data": user_data}


@router.put("/user/change_password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    db: db_dependency, user: user_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_data = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(user_verification.password, user_data.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")
    user_data.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.commit()


@router.put("/user/phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
def phone_number(db: db_dependency, user: user_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_data = db.query(Users).filter(Users.id == user.get("id")).first()

    user_data.phone_number = phone_number
    db.commit()
