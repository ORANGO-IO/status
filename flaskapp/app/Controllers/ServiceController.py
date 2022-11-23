from app.Models.Service import Service
from app.Models.ServiceGroup import ServiceGroup
from flask import Response

class ServiceController:
    def create(self,name,service_group_id):
        try:
            if ServiceGroup.find_by_id(service_group_id) is None:
                return Response('{"error":"service_group not exist"}', status=400, mimetype='application/json')
            if not Service.find_by_name(name.upper(),service_group_id) is None:
                return Response('{"error":"service already exist"}', status=400, mimetype='application/json')
            Service(**{"name":name.upper(),"service_group_id":service_group_id}).save()
            return Response(status=201)     
        except: 
            return Response('{"error":"server error"}', status=500, mimetype='application/json')