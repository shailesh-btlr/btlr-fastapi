from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models
from app.config import settings
from app.internal.security import get_password_hash
from app.schemas.users import UserCreate
from app.services import chat, graph, zep, otp


def new_graph():
    return graph.PreferenceGraph(
        settings.NEO4J_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD
    )


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        func.lower(models.User.email) == func.lower(email)
        ).first()


def get_users(db: Session):
    return db.query(models.User).all()


def create_user(db: Session, user: UserCreate):
    db_user = models.User(
        email=user.email,
        password=get_password_hash(otp.generate_otp())
    )
    db.add(db_user)
    db.flush()
    db.refresh(db_user)
    new_user_id = str(db_user.id)
    chat_user_name = chat.create_user_for_id(new_user_id)
    zep.create_user_with_session_and_add_collection(chat_user_name)
    db.commit()
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None


def update_user_password(db: Session, user_id: int, password: str):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.password = get_password_hash(password)
        db.commit()
        db.refresh(db_user)
        return db_user


def filter_users_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email.ilike(f"%{email}%")
    ).all()
