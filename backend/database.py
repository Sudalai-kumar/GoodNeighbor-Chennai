from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Check for environment variable (Production), otherwise fallback to local SQLite
default_db = f"sqlite:///{os.path.join(BASE_DIR, 'p2p.db')}"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", default_db)

# SQLite needs 'check_same_thread', but PostgreSQL (psycopg2) will crash if it sees it.
engine_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
