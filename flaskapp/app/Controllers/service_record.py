
from app.Models.Job import Job
from flask import jsonify
from app.Models.Service import Service
from app.services.job_record_strategy import record_job_strategy

class Service_record_controller:
    
    def create(self, service_group_id):
        jobs_filter_by_service = Job.query.join(Service).filter(Service.service_group_id == service_group_id).order_by(Job.order)
        jobs_records = []
        jobs_records_order_by_service = []
        for job in jobs_filter_by_service:
            job_record =record_job_strategy(job)
            date_time_format = job_record.created_at.strftime('Última atualização %d de %B de %Y %H:%M')

            jobs_records.append({
                'job_id':job_record.job_id,
                'service_id':job_record.job.service_id,
                'status':job_record.status.value,
                'date_time_format':date_time_format
            })
        for job_record in jobs_records:
            existService = False
            for job_record_order_by_service in jobs_records_order_by_service:
                if job_record_order_by_service['id'] == job_record['service_id']:
                    if not job_record_order_by_service['status'] ==job_record['status']:
                         job_record_order_by_service['status'] = 'warning'
                    existService = True
            if not existService:
                jobs_records_order_by_service.append({
                    'job_id':job_record['job_id'],
                    'id':job_record['service_id'],
                    'status':job_record['status'],
                    'date_time_format':job_record['date_time_format']
                })

                    
        return jsonify(jobs_records=jobs_records_order_by_service)

