"""
Modelos ORM do SQLAlchemy — mapeiam as tabelas do banco de dados PostgreSQL.
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Autor(Base):
    """Tabela de autores da biblioteca digital."""

    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    nacionalidade = Column(String(100), nullable=False)
    data_nascimento = Column(Date, nullable=False)

    # Relacionamento 1:N — um autor pode ter vários livros
    livros = relationship("Livro", back_populates="autor", cascade="all, delete-orphan")


class Livro(Base):
    """Tabela de livros vinculados a um autor (chave estrangeira)."""

    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    genero = Column(String(100), nullable=False)
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)

    # Relacionamento inverso — cada livro pertence a um autor
    autor = relationship("Autor", back_populates="livros")
