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
docker compose exec -it status python cli/main.py run-task {task_id}
```

- Executar todos as tasks de um serviço manualmente:

```bash
docker compose exec -it status python cli/main.py run-service
```

- Criar um token de autenticação:

```bash
docker compose exec status python cli/main.py create-token
```

- Criar ou cadastrar uma senha com criptografia:

```bash
docker compose exec status python cli/main.py create-password
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

### Exemplos de configuração

Para configuração de tasks precisamos de json line ao executar `create-task`

#### Configuração de task tipo `check`, `e2e` e `capture`

Essa tabela detalha os campos necessários para configurar uma task do tipo `check`, `e2e` ou `capture`. Cada campo deve ser preenchido corretamente para garantir o funcionamento esperado.

| Campo                          | Descrição                                                                                                                                           |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `action`                       | Tipo de ação: `goto`, `wait_for_selector`, `extract_text`, `click`, `find_and_click_link`, `find_and_extract_download_link`, `capture_current_url`. |
| `url`                          | URL a ser acessada (obrigatório apenas para `action: "goto"`).                                                                                      |
| `selector`                     | Seletor CSS do elemento (necessário para `wait_for_selector`, `extract_text`, `click`).                                                             |
| `regex`                        | Expressão regular para tratar o texto extraído (opcional em `extract_text`).                                                                        |
| `store_as`                     | Chave de contexto onde será armazenado o valor extraído (opcional em `extract_text`, `find_and_extract_download_link`, `capture_current_url`).      |
| `aria_label_contains_variable` | Nome da variável no contexto cujo valor deve estar contido no atributo `aria-label` do link (obrigatório em `find_and_click_link`).                  |
| `text_contains`                | Texto que deve estar presente no link ou botão a ser clicado ou extraído (necessário em `find_and_click_link` e `find_and_extract_download_link`).   |

#### Ações suportadas (`action`)

| `action`                          | Descrição                                                                                                      |
|----------------------------------|----------------------------------------------------------------------------------------------------------------|
| `goto`                           | Acessa uma URL definida no campo `url`.                                                                       |
| `wait_for_selector`              | Aguarda até que um seletor CSS esteja presente na página.                                                     |
| `extract_text`                   | Extrai o texto de um elemento definido por `selector`. Pode aplicar `regex` e armazenar com `store_as`.       |
| `click`                          | Clica em um elemento identificado pelo seletor CSS.                                                            |
| `find_and_click_link`            | Procura por um link (`<a>`) que contenha um texto específico e um `aria-label` com variável armazenada.        |
| `find_and_extract_download_link` | Clica em um botão que inicia um download e captura a URL do arquivo baixado. Pode armazenar com `store_as`.   |
| `capture_current_url`            | Armazena a URL atual da página no contexto, se definido `store_as`, ou retorna como resultado principal.      |



#### Configuração de task tipo `request`

Essa tabela detalha os campos necessários para configurar uma task do tipo `request`. Cada campo deve ser preenchido corretamente para garantir o funcionamento esperado. 

| Campo                  | Descrição                                                                                     |
|------------------------|-----------------------------------------------------------------------------------------------|
| `method`               | Método HTTP a ser utilizado na requisição (ex.: `GET`, `POST`, etc.).                         |
| `url`                  | URL do serviço a ser requisitado.                                                            |
| `headers`              | Cabeçalhos HTTP adicionais para a requisição (formato JSON).                                 |
| `expected_values`      | Valores esperados na resposta da requisição, definidos como um objeto JSON. Com suporte a expressões JSONPath (ex.: `._links.self[].href`).                 |

Exemplo:

```json
{
  "method": "GET",
  "url": "https://litho.com.br/wp/wp-json",
  "headers": {},
  "expected_values": {
    "name": "Lithocenter HospitalDia - WORDPRESS",
    "url": "https://litho.com.br/wp",
    "namespaces": ["wp/v2"],
    "routes./._links.self[].href": "https://litho.com.br/wp/wp-json/"
  }
}
```

## 📋 Stack utilizada

- Python 3.11
- Flask 2.x
- SQLAlchemy + Alembic (Flask-Migrate)
- APScheduler
- Typer (CLI)
- Playwright (para interações web e capturas)
- Docker + Docker Compose
- MariaDB
