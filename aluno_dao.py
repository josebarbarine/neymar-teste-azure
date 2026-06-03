import psycopg
from psycopg.rows import namedtuple_row

class AlunoDAO:
    def __init__(self, dados_conexao: str):
        # Salva a string de conexão informada no main.py
        self.dados_conexao = dados_conexao

    def inserir_aluno(self, nome: str, email: str):
        # Conecta ao banco de dados
        with psycopg.connect(self.dados_conexao) as conn:
            with conn.cursor() as cursor:
                # Executa o comando SQL para inserir. 
                # O id deve ser gerado automaticamente pelo banco (ex: SERIAL ou IDENTITY)
                cursor.execute(
                    "INSERT INTO alunos (nome, email) VALUES (%s, %s);",
                    (nome, email)
                )
                # Confirma a transação
                conn.commit()

    def listar_todos(self):
        with psycopg.connect(self.dados_conexao) as conn:
            # O row_factory=namedtuple_row é o "truque" que permite que o seu main.py 
            # consiga acessar os dados usando ponto, como: aluno.nome e aluno.email
            with conn.cursor(row_factory=namedtuple_row) as cursor:
                cursor.execute("SELECT id, nome, email FROM alunos;")
                # Retorna uma lista com todos os resultados
                return cursor.fetchall()
