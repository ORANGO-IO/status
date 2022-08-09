from app.Models.Service import Service
from app.Models.Service_group import Service_group
from flask import jsonify,Response

class ServiceController:
    def create(self,name,service_group_id):
        try:
            if Service_group.find_by_id(service_group_id) is None:
                return Response('{"error":"service_group not exist"}', status=400, mimetype='application/json')
            if not Service.find_by_name(name.upper(),service_group_id) is None:
                return Response('{"error":"service already exist"}', status=400, mimetype='application/json')
            newService = Service(**{"name":name.upper(),"service_group_id":service_group_id}).save()
            return jsonify(
                id=newService.id,
                createdAt=newService.created_at,
                name=newService.name,
            )
        except: 
            return Response('{"error":"server error"}', status=500, mimetype='application/json')