Dentro da pasta do projeto execute

```sh
docker-compose build --no-cache
docker-compose up -d
# Rodando na porta 5005 por padrão, alterar em .env
# use http://localhost:5005/service/lithocenter_frontend para testar o fluxo do frontend
docker-compose logs -f
```

## Rodar as migrations e seeds
Entre no terminal do container do flaskapp e rode os seguintes comandos:

```sh
python -m flask db migrate
python -m flask db seed
```