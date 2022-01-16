from app.Models.Job import Job
from app.Models.Service import Service
from flask import jsonify,Response

class JobController:
    def create(self,order,url,action,actionValue,serviceId):
        try:
            if Service.find_by_id(serviceId) is None:
                return Response('{"error":"service not exist"}', status=404, mimetype='application/json')
            jobValues = {
                'order':order,
                'url':url,
                'action':action,
                'action_value':actionValue,
                'service_id':serviceId
                }
            newJob =Job(**jobValues).save()
            return jsonify(
                id=newJob.id,
                order=newJob.order,
                url=newJob.url,
                action=newJob.action,
                actionValue=newJob.action_value,
                serviceId=newJob.service_id,
                createdAt=newJob.created_at
            )
        except: 
            return Response('{"error":"server error"}', status=500, mimetype='application/json')