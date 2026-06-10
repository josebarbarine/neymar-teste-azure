"""
Ponto de entrada da BookStore API.
Registra os routers, cria as tabelas no banco na inicialização
e configura os metadados do Swagger UI.
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import autores, livros

# Cria todas as tabelas definidas nos models caso não existam ainda
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BookStore API",
    description=(
        "API RESTful para gerenciamento de uma biblioteca digital.\n\n"
        "Permite o cadastro de **autores** e seus **livros**, "
        "com relacionamento 1:N e operações completas de CRUD."
    ),
    version="1.0.0",
    contact={
        "name": "Trabalho Prático — FastAPI + PostgreSQL",
    },
    license_info={
        "name": "MIT",
    },
)

# Registro dos routers
app.include_router(autores.router)
app.include_router(livros.router)


@app.get("/", tags=["Root"], summary="Health check da API")
def root():
    """Verifica se a API está no ar."""
    return {
        "status": "online",
        "mensagem": "Bem-vindo à BookStore API! Acesse /docs para ver a documentação.",
    }
