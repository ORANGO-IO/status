from app.Models.Service import Service
from flask import jsonify,Response

class ServiceController:
    def create(self,name):
        try:
            if not Service.find_by_name(name.upper()) is None:
                return Response('{"error":"service already exist"}', status=400, mimetype='application/json')
            newService = Service(**{"name":name.upper()}).save()
            return jsonify(
                id=newService.id,
                createdAt=newService.created_at,
                name=newService.name,
            )
        except: 
            return Response('{"error":"server error"}', status=500, mimetype='application/json')