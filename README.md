# 📚 BookStore API

API RESTful desenvolvida com **FastAPI** e **PostgreSQL** para gerenciamento de uma biblioteca digital.

> Trabalho Prático — Desenvolvimento de Software / Linguagem de Programação Python  
> Professor: Cleiton

---

## 🏗️ Estrutura do Projeto

```
bookstore_api/
├── main.py                  # Ponto de entrada da aplicação
├── requirements.txt         # Dependências do projeto
├── .env.example             # Modelo do arquivo de variáveis de ambiente
│
└── app/
    ├── __init__.py
    ├── database.py          # Configuração do SQLAlchemy (engine, sessão, Base)
    ├── models.py            # Modelos ORM (tabelas Autor e Livro)
    ├── schemas.py           # Schemas Pydantic (validação e serialização)
    │
    └── routers/
        ├── __init__.py
        ├── autores.py       # Endpoints CRUD de /autores
        └── livros.py        # Endpoints CRUD de /livros
```

---

## ⚙️ Configuração e Execução

### 1. Pré-requisitos

- Python 3.11+
- PostgreSQL rodando localmente (ou via Docker)

### 2. Clone o repositório

```bash
git clone <url-do-repositorio>
cd bookstore_api
```

### 3. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados

Crie o banco no PostgreSQL:

```sql
CREATE DATABASE bookstore_db;
```

Copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o `.env`:

```env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/bookstore_db
```

### 6. Execute a API

```bash
uvicorn main:app --reload
```

> As tabelas serão **criadas automaticamente** na primeira execução.

---

## 📖 Documentação Interativa

Com a API rodando, acesse:

| Interface | URL |
|-----------|-----|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## 🔀 Endpoints Disponíveis

### Autores

| Método | Rota | Descrição | Status |
|--------|------|-----------|--------|
| `POST` | `/autores/` | Criar autor | 201 |
| `GET` | `/autores/` | Listar todos | 200 |
| `GET` | `/autores/{id}` | Buscar por ID (com livros) | 200 / 404 |
| `PUT` | `/autores/{id}` | Atualizar autor | 200 / 404 |
| `DELETE` | `/autores/{id}` | Remover autor (cascade) | 204 / 404 |

### Livros

| Método | Rota | Descrição | Status |
|--------|------|-----------|--------|
| `POST` | `/livros/` | Criar livro | 201 / 404 |
| `GET` | `/livros/` | Listar todos | 200 |
| `GET` | `/livros/{id}` | Buscar por ID | 200 / 404 |
| `PUT` | `/livros/{id}` | Atualizar livro | 200 / 404 |
| `DELETE` | `/livros/{id}` | Remover livro | 204 / 404 |

---

## 🧪 Exemplos de Uso (via curl)

### Criar um autor

```bash
curl -X POST "http://localhost:8000/autores/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Machado de Assis",
    "nacionalidade": "Brasileiro",
    "data_nascimento": "1839-06-21"
  }'
```

### Criar um livro

```bash
curl -X POST "http://localhost:8000/livros/" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Dom Casmurro",
    "ano_publicacao": 1899,
    "genero": "Romance",
    "autor_id": 1
  }'
```

### Listar todos os livros

```bash
curl "http://localhost:8000/livros/"
```

### Buscar autor com seus livros

```bash
curl "http://localhost:8000/autores/1"
```

### Atualizar um livro

```bash
curl -X PUT "http://localhost:8000/livros/1" \
  -H "Content-Type: application/json" \
  -d '{"genero": "Realismo"}'
```

### Deletar um autor (remove livros em cascata)

```bash
curl -X DELETE "http://localhost:8000/autores/1"
```

---

## 🗄️ Modelo de Dados

```
┌──────────────────────┐         ┌──────────────────────────┐
│        autores       │         │          livros           │
├──────────────────────┤         ├──────────────────────────┤
│ id (PK)              │◄────────│ id (PK)                  │
│ nome                 │  1 : N  │ titulo                   │
│ nacionalidade        │         │ ano_publicacao            │
│ data_nascimento      │         │ genero                   │
└──────────────────────┘         │ autor_id (FK)            │
                                 └──────────────────────────┘
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|------------|--------|--------|
| FastAPI | 0.115.0 | Framework web |
| SQLAlchemy | 2.0.35 | ORM |
| PostgreSQL | 15+ | Banco de dados |
| Pydantic | 2.9.2 | Validação de dados |
| Uvicorn | 0.30.6 | Servidor ASGI |
| python-dotenv | 1.0.1 | Variáveis de ambiente |
