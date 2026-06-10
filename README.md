# TaskManager Azure 🚀

Aplicação web Python/Flask com CRUD de tarefas, autenticação GitHub OAuth,
deploy containerizado no **Microsoft Azure** via pipeline CI/CD automático.

## Infraestrutura Azure

| Recurso              | Nome           | Tipo                      |
|----------------------|----------------|---------------------------|
| Resource Group       | azure1910      | Grupo de recursos         |
| Container Registry   | conteiney      | Azure Container Registry  |
| Web App              | appneymar      | App Service (container)   |
| Banco de Dados       | opet1910       | PostgreSQL Flexible Server|

**URL pública:** `https://appneymar.azurewebsites.net`

## Stack

- Python 3.11 + Flask 3.0
- SQLAlchemy + PostgreSQL
- GitHub OAuth (Authlib)
- Docker (multi-stage build)
- GitHub Actions (CI/CD)
- Azure Container Registry + Web App for Containers

## Rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USER/SEU_REPO.git
cd SEU_REPO

# 2. Configure variáveis de ambiente
cp .env.example .env
# Edite .env com seus dados

# 3. Suba com Docker Compose
docker-compose up --build
```

Acesse: http://localhost:8000

## GitHub Secrets necessários

Configure em: **Settings → Secrets and variables → Actions**

| Secret              | Descrição                                           |
|---------------------|-----------------------------------------------------|
| `ACR_USERNAME`      | Login do Azure Container Registry (conteiney)       |
| `ACR_PASSWORD`      | Senha do ACR (Admin password)                       |
| `AZURE_CREDENTIALS` | JSON do Service Principal Azure                     |
| `SECRET_KEY`        | Chave secreta Flask                                 |
| `DATABASE_URL`      | Connection string PostgreSQL (opet1910)             |
| `GITHUB_CLIENT_ID`  | ID do GitHub OAuth App                              |
| `GITHUB_CLIENT_SECRET` | Secret do GitHub OAuth App                      |

## Como obter AZURE_CREDENTIALS

```bash
az ad sp create-for-rbac \
  --name "github-actions-sp" \
  --role contributor \
  --scopes /subscriptions/1db5922f-f872-44fc-8006-7005513ea68e/resourceGroups/azure1910 \
  --sdk-auth
```

Cole o JSON resultante como valor do secret `AZURE_CREDENTIALS`.

## Fluxo CI/CD

```
git push main
    ↓
GitHub Actions
    ├── 1. Build & Lint Python
    ├── 2. docker build → conteiney.azurecr.io/appneymar:<sha>
    └── 3. az webapp deploy → appneymar.azurewebsites.net
```

## CRUD disponível

| Operação | Rota                      | Método |
|----------|---------------------------|--------|
| Listar   | /tasks/                   | GET    |
| Criar    | /tasks/create             | GET/POST |
| Editar   | /tasks/\<id\>/edit        | GET/POST |
| Deletar  | /tasks/\<id\>/delete      | POST   |
| API JSON | /tasks/api                | GET    |
