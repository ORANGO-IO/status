# This file should contain records you want created when you run flask db seed.
#
# Example:
from flask import current_app
from app.Models.JopRecordStatus import JopRecordStatus
# from app.services.db import db
app_config = current_app.config

print("oioi")
initialStatus = [
    {
        "value":"online",
        "description":"online"
    },
    {
        "value":"offline",
        "description":"offline"
    }
]

for x in initialStatus:
    if JopRecordStatus.find_by_name(x['value']) is None:
        JopRecordStatus(**x).save()

# db.session.add(status)
# db.session.commit()
