# backend/app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ---- MySQL Connection Details ----
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "mysql")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "pm_db")

# ---- Create the database URL ----
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ---- SQLAlchemy Engine and Session ----
engine = create_engine(DATABASE_URL, echo=True)  # echo=True shows SQL logs
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---- Base class for ORM models (we'll use this later) ----
Base = declarative_base()

# ---- Dependency function for database session ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
