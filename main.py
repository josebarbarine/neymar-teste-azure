import os
import psycopg
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from aluno_dao import AlunoDAO

# Procura a variável de ambiente do Azure. Se não existir, usa o fallback local para testes.
dados_conexao = os.environ.get(
    "DATABASE_URL", 
    "host=127.0.0.1 port=5432 dbname=postgres user=postgres password=1910"
)

# Inicialização crucial do FastAPI que o Uvicorn precisa encontrar (main:app)
app = FastAPI()

# Inicializa o DAO com a string de conexão configurada
dao = AlunoDAO(dados_conexao)
print("DAO Aluno carregado com sucesso!")

# Modelo Pydantic para validação dos dados
class Aluno(BaseModel):
    id: Optional[int] = None  # Tornamos opcional pois o banco gera automaticamente (SERIAL)
    nome: str
    email: str

@app.post("/alunos", status_code=201)
def criar_aluno(aluno: Aluno):
    dao.inserir_aluno(aluno.nome, aluno.email)
    return {"message": "Aluno criado com sucesso!"}

@app.get("/alunos")
def listar_alunos():
    resultados = dao.listar_todos()
    if not resultados:
        return {"message": "Nenhum aluno encontrado."}
        
    mensagem = ""
    for aluno in resultados:
        mensagem = mensagem + f"aluno {aluno.nome}; "

    return {"message": mensagem.strip()}
