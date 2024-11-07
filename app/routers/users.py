from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.users import User, UserCreate, UserBase, UserList
from app.services import users
from typing import Optional

router = APIRouter()


@router.post("", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users.create_user(db, user)


@router.get("", response_model=UserList)
def filter_users_by_email(
    email: Optional[str] = "",
    db: Session = Depends(get_db)
):
    return users.filter_users_by_email(db, email)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    users.delete_user(db, user_id=user_id)
