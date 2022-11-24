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
docker exec -it status_flaskapp bash
python -m flask db migrate
python -m flask db seed
```
## Criando uma gravação de um job
    Para criar uma gravação de um job, execute a rota api/job_record/<job_id> sendo o job_id o id de algum job
    Ou entre na rota "/" e clique no botão testar de algum grupo de serviços

## Rodando docker no windows
```sh
# Desligando os containers e removendo seus volumes
docker-compose down --remove-orphans --volumes
docker-compose -f docker-compose.windows.yml down --remove-orphans --volumes
# Executando novamente os containers
docker-compose -f docker-compose.windows.yml up --build
# Se quiser dar um hard reset para garantir que nenhum cache ficou vc pode
docker-compose -f docker-compose.windows.yml build --no-cache
docker-compose -f docker-compose.windows.yml up
```

## Rodando docker no linux
```sh
docker-compose down --remove-orphans --volumes
docker-compose up --build
```

### Como criar um job
Para criar o job,precisa ter cadastrado um grupo de serviços e um serviço

- Para criar um grupo de serviços,use a rota /api/service_group passando o parametro name com o nome do grupo de serviço no seguinte formato:
    {
        "name":string
    }
- Para criar um serviço,precisa passar o id do grupo de serviços e o nome do serviço como parametro no seguinte formato:
    {
	    "name":string,
	    "service_group_id":int
    }

- Para criar um job,precisa passar os seguintes campos para o backend
    {
        "order":int,		     
        "url":string,
        "action":string,
        "actionValue":string,
        "serviceId":int,
        "description":string
    }

o parametro action será o tipo de ação que ele executará
o parametro actionValue servirá apenas quando o parametro action for XPATH,se não, pode ser vazio