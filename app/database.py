import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Ensure data directory exists if using SQLite
if settings.DATABASE_URL.startswith("sqlite"):
    db_relative_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if db_relative_path and db_relative_path != ":memory:":
        db_file_dir = os.path.dirname(os.path.abspath(db_relative_path))
        os.makedirs(db_file_dir, exist_ok=True)

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency for yielding database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
