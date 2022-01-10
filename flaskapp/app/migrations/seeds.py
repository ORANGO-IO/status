# This file should contain records you want created when you run flask db seed.
#
# Example:
from flask import current_app
from app.Models.Status import Status
from app.Models.Service import Service
# from app.services.db import db
app_config = current_app.config

print("oioi")
initialStatus = [
    {
        "value":"on"
    },
    {
        "value":"off"
    }
]

initialServices = [
    {
        "name":"LITHOCENTER"
    }
]

for x in initialStatus:
    if Status.find_by_username(x['value']) is None:
        Status(**x).save()

for x in initialServices:
    if Service.find_by_username(x['name']) is None:
        Service(**x).save()
      
# db.session.add(status)
# db.session.commit()
