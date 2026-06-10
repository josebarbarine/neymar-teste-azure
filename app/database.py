"""
Configuração da conexão com o banco de dados PostgreSQL via SQLAlchemy.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/bookstore_db"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependency que fornece uma sessão de banco de dados por requisição.
    Garante que a sessão seja fechada ao final de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
