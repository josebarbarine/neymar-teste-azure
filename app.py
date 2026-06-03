import psycopg
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from aluno_dao import AlunoDAO


dados_conexao = "host=127.0.0.1 port=5432 dbname=postgres user=postgres password=1910"

app = FastAPI()
dao = AlunoDAO(dados_conexao)
print("dao aluno carregado")

class Aluno(BaseModel):
    id: int
    nome: str
    email: str

@app.post("/alunos", status_code=201)
def criar_aluno(aluno: Aluno):
    dao.inserir_aluno(aluno.nome, aluno.email)
    return {"message": "Aluno criado com sucesso!"}

@app.get("/alunos")
def listar_alunos():
    resultados = dao.listar_todos()
    mensagem = ""
    for aluno in resultados:
        mensagem = mensagem + f"aluno {aluno.nome}"

    return {"message": mensagem}

