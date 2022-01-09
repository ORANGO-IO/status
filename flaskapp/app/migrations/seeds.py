# This file should contain records you want created when you run flask db seed.
#
# Example:
from flask import current_app
from app.Models.Status import Status
# from app.services.db import db
app_config = current_app.config

print("oioi")
initial_user = [
    {
        "value":"b"
    },
    {
        "value":"a"
    }
]

for x in initial_user:
    Status(**x).save()
# db.session.add(status)
# db.session.commit()
# if Status.find_by_username(initial_user['username']) is None:
#     User().save()
