from app.Models.Service import Service
from flask import jsonify
class ServiceController:
    def create(self,name):
        if not Service.find_by_name(name) is None:
            return
        newService = Service(**{"name":name}).save()
        return jsonify(
            id=newService.id,
            createdAt=newService.created_at,
            name=newService.name,
        )