"""
Rotas CRUD para a entidade Autor.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
)


@router.post(
    "/",
    response_model=schemas.AutorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo autor",
)
def criar_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    """Cria um novo autor e persiste no banco de dados."""
    novo_autor = models.Autor(**autor.model_dump())
    db.add(novo_autor)
    db.commit()
    db.refresh(novo_autor)
    return novo_autor


@router.get(
    "/",
    response_model=list[schemas.AutorResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os autores",
)
def listar_autores(db: Session = Depends(get_db)):
    """Retorna a lista completa de autores cadastrados."""
    return db.query(models.Autor).all()


@router.get(
    "/{autor_id}",
    response_model=schemas.AutorComLivrosResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar autor por ID (inclui seus livros)",
)
def buscar_autor(autor_id: int, db: Session = Depends(get_db)):
    """
    Retorna um autor específico pelo ID.
    A resposta inclui a lista de livros associados ao autor.
    Retorna **404** caso o ID não exista.
    """
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com id={autor_id} não encontrado.",
        )
    return autor


@router.put(
    "/{autor_id}",
    response_model=schemas.AutorResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados de um autor",
)
def atualizar_autor(
    autor_id: int,
    dados: schemas.AutorUpdate,
    db: Session = Depends(get_db),
):
    """
    Atualiza parcialmente os dados de um autor existente.
    Apenas os campos enviados no corpo serão atualizados.
    Retorna **404** caso o ID não exista.
    """
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com id={autor_id} não encontrado.",
        )

    campos_atualizados = dados.model_dump(exclude_unset=True)
    for campo, valor in campos_atualizados.items():
        setattr(autor, campo, valor)

    db.commit()
    db.refresh(autor)
    return autor


@router.delete(
    "/{autor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um autor",
)
def deletar_autor(autor_id: int, db: Session = Depends(get_db)):
    """
    Remove um autor e todos os seus livros (cascade).
    Retorna **204 No Content** em caso de sucesso.
    Retorna **404** caso o ID não exista.
    """
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if not autor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor com id={autor_id} não encontrado.",
        )

    db.delete(autor)
    db.commit()
