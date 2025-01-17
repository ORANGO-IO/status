
from app.Models.JobRecord import JobRecord
from app.Models.Job import Job
from flask import jsonify, Response
from app.Models.Service import Service
from app.services.job_record_strategy import record_job_strategy
from app.Models.ServiceGroup import ServiceGroup
from app.Models.JopRecordStatus import JopRecordStatus
from app.config.app import db
from sqlalchemy import func,distinct
from app.Models.Screenshot import Screenshot

class JobRecordController:
    
    def create(self, job_id):
        job = ''
        try:
            job = Job.find_by_id(job_id)
            if job is None:
                return Response('{"error":"job not exist"}', status=404, mimetype='application/json')
        except Exception:
            return Response('{"error":"server error in job"}', status=404, mimetype='application/json')
        job_record = record_job_strategy(job)
        return jsonify(
                id=job_record.id,
                time_spent_in_sec=job_record.time_spent_in_sec,
                service_id=job_record.id,
                status_id=job_record.status_id,
                createdAt=job_record.created_at
            )

    def get_job_records_by_service(self,service_id,page):
        jobs_records_response = JobRecord.query.join(Job).outerjoin(Screenshot).filter(Job.service_id == service_id ).order_by(JobRecord.created_at.desc()).paginate(page=page,per_page=10)
        service = Service.find_by_id(service_id)
        jobs_records = []
        print("jobs_records_response")
        print(jobs_records_response)
        for job_record in jobs_records_response.items:
            date_time_format = job_record.created_at.strftime('Verificado em %d de %B de %Y %H:%M')
            current_job_record = {
                'id': job_record.id,
                'status': job_record.status.value,
                'time_spent_in_sec': job_record.time_spent_in_sec,
                'date_time_format':date_time_format,
                'job': {
                    "id": job_record.job.id,
                    "order": job_record.job.order,
                    "url": job_record.job.url,
                    "action": job_record.job.action,
                    "action_value": job_record.job.action_value,
                    "description":job_record.job.description
                },
                'created_at':job_record.created_at
            }
            if not job_record.screenshots.__len__() == 0:
                current_job_record['image']= job_record.screenshots[0].url
            
            jobs_records.append(current_job_record)
        
        return {"jobs_records":jobs_records,"name":service.name,"group":service.service_group.name,'count':JobRecord.query.join(Job).filter(Job.service_id == service_id ).count()}

    def all(self):
        print("==================== CAPTURANDO TODOS OS JOB RECORDS ====================")
        jobs_records_by_service_group = ServiceGroup.query.outerjoin(Service).outerjoin(Job).outerjoin(JobRecord).outerjoin(JopRecordStatus).all()

        jobs_record_array =[]
        
        count_online = 0
        count_offline = 0

        for job_record in jobs_records_by_service_group:
            job_record_object = {
                "service_group":job_record.name,
                "id":job_record.id,
                "services":[],
                "if_not_exist_services":"Sem serviços cadastrados para verificação"
            }     
            if hasattr(job_record,"services"):
                date = None
                for service in job_record.services:
                    service_object ={
                        "id":service.id,
                        "name":service.name,
                        "status":"not",
                        "last_updated":"",
                        "date_time_format":"Serviço não verificado",
                    }
                    if hasattr(service,"jobs"):
                        for job in service.jobs:
                            if hasattr(job,"job_record"):
                                if job.job_record.__len__() > 0:
                                    job_record_by_service = job.job_record[job.job_record.__len__()-1]
                                    service_object["last_updated"] = job_record_by_service.created_at
                                    date_time_format = job_record_by_service.created_at.strftime('Última atualização %d de %B de %Y %H:%M')
                                    service_object["date_time_format"] = date_time_format
                                    if job_record_by_service.status.value == 'online':  
                                        count_online +=1
                                    else:
                                        count_offline +=1
                                    if not service_object['status'] == 'not' and not service_object['status'] == job_record_by_service.status.value:
                                        service_object['status'] = 'warning'
                                    else:
                                        service_object['status'] = job_record_by_service.status.value
                    job_record_object['services'].append(service_object)
            jobs_record_array.append(job_record_object)
                
        
        
        print("==================== CAPTURANDO TODOS OS JOB RECORDS - END ====================")
        return {"jobs_record_array":jobs_record_array,"count_online":count_online,"count_offline":count_offline}