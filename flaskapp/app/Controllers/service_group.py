from app.Models.ServiceGroup import ServiceGroup
from flask import jsonify,Response

class Service_Group_Controller:
    def create(self,name):
        try:
            if not ServiceGroup.find_by_name(name.upper()) is None:
                return Response('{"error":"service_group already exist"}', status=400, mimetype='application/json')
            new_service_group = ServiceGroup(**{"name":name}).save()
            return jsonify(
                id=new_service_group.id,
                name=new_service_group.name,
                createdAt=new_service_group.created_at,
            )
        except: 
            return Response('{"error":"server error"}', status=500, mimetype='application/json')

        