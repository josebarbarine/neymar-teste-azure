"""
Schemas Pydantic para validação de entrada e serialização de saída da API.
Separados por entidade e por operação (Create, Update, Response).
"""

from datetime import date
from pydantic import BaseModel, Field, field_validator


# ─────────────────────────────────────────
#  AUTORES
# ─────────────────────────────────────────

class AutorBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150, examples=["Machado de Assis"])
    nacionalidade: str = Field(..., min_length=2, max_length=100, examples=["Brasileiro"])
    data_nascimento: date = Field(..., examples=["1839-06-21"])


class AutorCreate(AutorBase):
    """Schema usado no corpo da requisição POST /autores."""
    pass


class AutorUpdate(BaseModel):
    """Schema usado no corpo da requisição PUT /autores/{id}. Todos os campos são opcionais."""

    nome: str | None = Field(default=None, min_length=2, max_length=150)
    nacionalidade: str | None = Field(default=None, min_length=2, max_length=100)
    data_nascimento: date | None = None


class AutorResponse(AutorBase):
    """Schema retornado nas respostas da API — inclui o id gerado pelo banco."""

    id: int

    model_config = {"from_attributes": True}


class AutorComLivrosResponse(AutorResponse):
    """Schema estendido que inclui a lista de livros do autor."""

    livros: list["LivroResponse"] = []

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────
#  LIVROS
# ─────────────────────────────────────────

class LivroBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200, examples=["Dom Casmurro"])
    ano_publicacao: int = Field(..., ge=0, le=2100, examples=[1899])
    genero: str = Field(..., min_length=2, max_length=100, examples=["Romance"])
    autor_id: int = Field(..., gt=0, examples=[1])

    @field_validator("ano_publicacao")
    @classmethod
    def validar_ano(cls, v: int) -> int:
        import datetime
        ano_atual = datetime.date.today().year
        if v > ano_atual:
            raise ValueError(f"O ano de publicação não pode ser no futuro (máximo: {ano_atual}).")
        return v


class LivroCreate(LivroBase):
    """Schema usado no corpo da requisição POST /livros."""
    pass


class LivroUpdate(BaseModel):
    """Schema usado no corpo da requisição PUT /livros/{id}. Todos os campos são opcionais."""

    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    ano_publicacao: int | None = Field(default=None, ge=0, le=2100)
    genero: str | None = Field(default=None, min_length=2, max_length=100)
    autor_id: int | None = Field(default=None, gt=0)

    @field_validator("ano_publicacao", mode="before")
    @classmethod
    def validar_ano(cls, v):
        if v is None:
            return v
        import datetime
        ano_atual = datetime.date.today().year
        if v > ano_atual:
            raise ValueError(f"O ano de publicação não pode ser no futuro (máximo: {ano_atual}).")
        return v


class LivroResponse(LivroBase):
    """Schema retornado nas respostas da API — inclui o id gerado pelo banco."""

    id: int

    model_config = {"from_attributes": True}


# Resolve a referência circular entre AutorComLivrosResponse e LivroResponse
AutorComLivrosResponse.model_rebuild()
