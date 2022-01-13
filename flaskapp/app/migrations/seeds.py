# This file should contain records you want created when you run flask db seed.
#
# Example:
from flask import current_app
from flaskapp.app.Models.JopRecordStatus import JopRecordStatus
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
    },
    {
        "name":"POSTBAKER"
    },
]

for x in initialStatus:
    if JopRecordStatus.find_by_name(x['value']) is None:
        JopRecordStatus(**x).save()

for x in initialServices:
    if Service.find_by_name(x['name']) is None:
        Service(**x).save()
      
# db.session.add(status)
# db.session.commit()
