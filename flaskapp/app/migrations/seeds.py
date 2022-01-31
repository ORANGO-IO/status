# This file should contain records you want created when you run flask db seed.
#
# Example:
from flask import current_app
from app.Models.JopRecordStatus import JopRecordStatus
from app.Models.Service_group import Service_group
from app.Models.Service import Service
from app.Models.Job import Job
from app.Models.JobRecord import JobRecord
# from app.services.db import db
app_config = current_app.config

print("run seeds")
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

service_group = {
    "name":"Lithocenter"
}

service = {
    "name":"teste",
    "service_group_id":1
}

job = {
	"order":1,
	"url":"http://lithocenterhospitaldia.com/",
	"action":"XPATH",
	"actionValue":"//div[@class='phone']/a[@class='number']",
	"serviceId":1
}

jobRecord={
    "job_id":1,
    "status_id":1,
    "time_spent_in_sec":321312,
}

for x in initialStatus:
    if JopRecordStatus.find_by_name(x['value']) is None:
        JopRecordStatus(**x).save()
Service_group(**service_group).save()
Service(**service).save()
Job(**job).save()
JobRecord(**jobRecord).save()
JobRecord(**jobRecord).save()
print("finished seeds")