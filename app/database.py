from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    connect_args=(
        {"check_same_thread": False}
        if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite")
        else {}
    ),
)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
