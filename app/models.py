"""Modelos ORM — tabelas autores e livros."""
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    nacionalidade = Column(String(100))
    data_nascimento = Column(Date)

    livros = relationship("Livro", back_populates="autor",
                          cascade="all, delete-orphan")


class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    ano_publicacao = Column(Integer)
    genero = Column(String(100))
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)

    autor = relationship("Autor", back_populates="livros")
