# This file should contain records you want created when you run flask db seed.
#
# Example:
from flask import current_app
from app.Models.JopRecordStatus import JopRecordStatus
from app.Models.ServiceGroup import ServiceGroup
from app.Models.Service import Service
from app.Models.Job import Job

app_config = current_app.config

print("run seeds")
initialStatus = [
    {
        "value": "online",
        "description": "online"
    },
    {
        "value": "offline",
        "description": "offline"
    }
]

service_group = [
    {
        "name": "lithocenter"
    },
    {
        "name": "postbaker"
    },
    {
        "name": "orango"
    },
    {
        "name": "Blog Orango"
    },
    {
        "name": "itmpr"
    },
    {
        "name": "Filipe lopes"
    },
    {
        "name": "Calc"
    },
    {
        "name": "clicklav"
    },
    {
        "name": "teleatendimento"
    }
]

service = [
    {
        "name": "frontend",
        "service_group_id": 3
    },
    {
        "name": "frontend",
        "service_group_id": 4
    }, {
        "name": "backend",
        "service_group_id": 4
    }, {
        "name": "database",
        "service_group_id": 4
    },
    {
        "name": "Painel adiministrativo",
        "service_group_id": 4,
    },
    {
        "name": "frontend",
        "service_group_id": 2,
    },
    {
        "name": "backend",
        "service_group_id": 2,
    },
    {
        "name": "database",
        "service_group_id": 2
    },
    {
        "name": "frontend",
        "service_group_id": 5,
    },
    {
        "name": "frontend beta",
        "service_group_id": 5,
    },
    {
        "name": "frontend beta",
        "service_group_id": 9
    },
    {
        "name": "backend beta",
        "service_group_id": 9
    },
    {
        "name": "banco de dados beta",
        "service_group_id": 9
    },
    {
        "name": "frontend",
        "service_group_id": 9
    },
    {
        "name": "backend",
        "service_group_id": 9
    },
    {
        "name": "banco de dados",
        "service_group_id": 9
    },
    {
        "name": "frontend",  # 17
        "service_group_id": 6
    },
    {
        "name": "backend",
        "service_group_id": 6
    },
    {
        "name": "banco de dados",
        "service_group_id": 6
    },
    {
        "name": "frontend",
        "service_group_id": 7
    },
    {
        "name": "frontend beta",
        "service_group_id": 8  # 21
    },
    {
        "name": "backend beta",
        "service_group_id": 8
    },
    {
        "name": "banco de dados beta",
        "service_group_id": 8
    },
    {
        "name": "frontend",
        "service_group_id": 8
    },
    {
        "name": "backend",
        "service_group_id": 8
    },
    {
        "name": "banco de dados",
        "service_group_id": 8
    },

]
job = [{
    "order": 1,
    "url": "https://orango.io/",
    "action": "XPATH",
    "action_value": "//div[@class='header']/img[@alt='logo']",
    "service_id": 1,
    'description': "descrição"
},
    {
    "order": 2,
    "url": "https://strapi.orango.io/",
    "action": "XPATH",
    "action_value": "//section[@class='wrapper']/h1/img[@class='logo']",
    "service_id": 5,
    'description': "descrição"
},
    {
    "order": 3,
    "url": "https://strapi.orango.io/admin/auth/login",
    "action": "XPATH",
    "action_value": "//*[@id='app']/div/div[3]/div/div[2]/section[1]/img",
    "service_id": 5,
    'description': "descrição"
},
    {
    "order": 1,
    "url": "https://beta.itmpr.com.br/adm/",
    "action": "XPATH",
    "action_value": "//div[@id='intro-logo']/img",
    "service_id": 10,
    'description': "descrição"
},
    {
    "order": 2,
    "url": "https://itmpr.com.br",
    "action": "XPATH",
    "action_value": "//header[@id='mainheader']/img[@id='mainlogo']",
    "service_id": 9,
    'description': "descrição"
},
    {
    "order": 2,
    "url": "https://teleatendimento.orango.io/login",
    "action": "XPATH",
    "action_value": "//header/img[@alt='lines']",
    "service_id": 11,
    'description': "descrição"
},
    {
    "order": 1,
    "url": "https://teleatendimento.orango.io/api/v1/",
    "action": "status",
    "action_value": "",
    "service_id": 12,
    'description': "descrição"
},
    {
    "order": 1,
    "url": "https://teleatendimento.orango.io/api/v1/alembic_version",
    "action": "status",
    "action_value": "alembic_version",
    "service_id": 16,
    'description': "descrição"
},
    {
    "order": 1,
    "url": "https://filipelopes.me/",
    "action": "XPATH",
    "action_value": "//*[@id='root']/main/header/nav/div[1]/a[1]",
    "service_id": 17,
    'description': "descrição"
},
    {
    "order": 1,
    "url": "https://clicklav.com.br/",
    "action": "XPATH",
    "action_value": "//*[@id='root']/div/header/nav/button[@class='menuToogle']",
    "service_id": 21,
    'description': "descrição"
},
    {
    "order": 1,
    "url": "https://blog.orango.io/",
    "action": "XPATH",
    "action_value": "//div[@class='header']/img[@class='logo']",
    "service_id": 2,
    'description': "descrição"
},
]

print("seed status")
for x in initialStatus:
    if JopRecordStatus.find_by_name(x['value']) is None:
        JopRecordStatus(**x).save()
print("seed service_group")
for x in service_group:
    if ServiceGroup.find_by_name(x['name']) is None:
        ServiceGroup(**x).save()
print("seed service")
for x in service:
    if Service.find_by_name(x['name'], x['service_group_id']) is None:
        Service(**x).save()
print("seed job")
for x in job:
    Job(**x).save()
print("finished seeds")
