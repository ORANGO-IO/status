# 📈 Status Monitoring System

Esse sistema contém um serviço web (Interface e API) e um por terminal (administrativo) para gerenciar o controle de verificação de serviços em execução.

Sistema de **monitoramento de serviços** com:

- **Interface web** para visualização de status
- **API segura** para consulta e integração
- **CLI** administrativa para criação de serviços, tasks e tokens
- **Scheduler** automático para verificação diária dos serviços

## 🚀 Instalação

1. Clone o projeto:

```bash
git clone https://github.com/ORANGO-IO/status.git
cd status
```

2. Inicie o ambiente com Docker Compose:

```bash
docker compose up -d --build
docker compose logs -f
```

Isso irá:

- Subir o container web (Flask) com APScheduler configurado
- Subir o banco de dados (MariaDB)
- Rodar as migrações (se configuradas)

## ⚙️ Banco de dados: Migrações (Flask-Migrate / Alembic)

### Inicializar (apenas na primeira vez)

```bash
docker compose exec status flask db init
```

### Criar uma nova migration (após alterações nos models)

```bash
docker compose exec status flask db migrate -m "Descrição da alteração"
```

### Aplicar migrations no banco

```bash
docker compose exec status flask db upgrade
```

## 🛠️ CLI Administrativo (Typer)

### Comandos disponíveis

- Criar novo serviço:

```bash
docker compose exec -it status python cli/main.py create-service
```

- Criar nova task:

```bash
docker compose exec -it status python cli/main.py create-task
```

- Executar uma task manualmente:

```bash
docker compose exec -it status python cli/main.py run-task
```

- Criar um token de autenticação:

```bash
docker compose exec status python cli/main.py create-token
```

##  🧪 Rodando testes

```bash
docker compose exec -it status pytest -s
```

## 🌐 Acesso à Interface Web

Após a inicialização:

```
http://localhost:5000
```

## 🔐 API Protegida

Utilize o token de autenticação no header `Authorization: Bearer`.

### Endpoints principais:

- `GET /service/<service_id>/task` → Lista tasks
- `GET /service/<service_id>/task/<task_id>` → Detalha uma task e seus resultados

Exemplo de chamada usando `curl`:

```bash
curl -H "Authorization: Bearer SEU_TOKEN" http://localhost:5000/service/{service_id}/task
```

## ⏰ Scheduler

- As tasks dos tipos `check`, `request` e `capture` são executadas automaticamente **todos os dias às 2h da manhã** (Timezone: America/Sao_Paulo).
- Gerenciado com **APScheduler**.

## 📋 Stack utilizada

- Python 3.11
- Flask 2.x
- SQLAlchemy + Alembic (Flask-Migrate)
- APScheduler
- Typer (CLI)
- Playwright (para interações web e capturas)
- Docker + Docker Compose
- MariaDB
