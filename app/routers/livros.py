"""
Rotas CRUD para a entidade Livro.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/livros",
    tags=["Livros"],
)


@router.post(
    "/",
    response_model=schemas.LivroResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo livro",
)
def criar_livro(livro: schemas.LivroCreate, db: Session = Depends(get_db)):
    """
    Cria um novo livro vinculado a um autor existente.
    Retorna **404** caso o `autor_id` informado não exista.
    """
    autor = db.query(models.Autor).filter(models.Autor.id == livro.autor_id).first()
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com id={livro.autor_id} não encontrado. Cadastre o autor antes de adicionar livros.",
        )

    novo_livro = models.Livro(**livro.model_dump())
    db.add(novo_livro)
    db.commit()
    db.refresh(novo_livro)
    return novo_livro


@router.get(
    "/",
    response_model=list[schemas.LivroResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os livros",
)
def listar_livros(db: Session = Depends(get_db)):
    """Retorna a lista completa de livros cadastrados."""
    return db.query(models.Livro).all()


@router.get(
    "/{livro_id}",
    response_model=schemas.LivroResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar livro por ID",
)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    """
    Retorna um livro específico pelo ID.
    Retorna **404** caso o ID não exista.
    """
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com id={livro_id} não encontrado.",
        )
    return livro


@router.put(
    "/{livro_id}",
    response_model=schemas.LivroResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados de um livro",
)
def atualizar_livro(
    livro_id: int,
    dados: schemas.LivroUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza parcialmente os dados de um livro existente.
    Se `autor_id` for alterado, valida se o novo autor existe.
    Retorna **404** caso o ID do livro ou do novo autor não exista.
    """
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com id={livro_id} não encontrado.",
        )

    campos_atualizados = dados.model_dump(exclude_unset=True)

    # Valida o novo autor_id caso ele tenha sido informado
    if "autor_id" in campos_atualizados:
        autor = db.query(models.Autor).filter(
            models.Autor.id == campos_atualizados["autor_id"]
        ).first()
        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Autor com id={campos_atualizados['autor_id']} não encontrado.",
            )

    for campo, valor in campos_atualizados.items():
        setattr(livro, campo, valor)

    db.commit()
    db.refresh(livro)
    return livro


@router.delete(
    "/{livro_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um livro",
)
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    """
    Remove um livro do banco de dados.
    Retorna **204 No Content** em caso de sucesso.
    Retorna **404** caso o ID não exista.
    """
    livro = db.query(models.Livro).filter(models.Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro com id={livro_id} não encontrado.",
        )

    db.delete(livro)
    db.commit()
