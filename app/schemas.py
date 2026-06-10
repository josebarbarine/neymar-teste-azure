"""Schemas Pydantic para validação e serialização."""
from datetime import date
from pydantic import BaseModel


# ── Livro ──────────────────────────────────────────────────────────────────

class LivroBase(BaseModel):
    titulo: str
    ano_publicacao: int | None = None
    genero: str | None = None


class LivroCreate(LivroBase):
    autor_id: int


class LivroUpdate(BaseModel):
    titulo: str | None = None
    ano_publicacao: int | None = None
    genero: str | None = None


class LivroOut(LivroBase):
    id: int
    autor_id: int

    model_config = {"from_attributes": True}


# ── Autor ──────────────────────────────────────────────────────────────────

class AutorBase(BaseModel):
    nome: str
    nacionalidade: str | None = None
    data_nascimento: date | None = None


class AutorCreate(AutorBase):
    pass


class AutorUpdate(BaseModel):
    nome: str | None = None
    nacionalidade: str | None = None
    data_nascimento: date | None = None


class AutorOut(AutorBase):
    id: int
    livros: list[LivroOut] = []

    model_config = {"from_attributes": True}
