from datetime import datetime
import time
from app.settings import ROOT_PATH
from app.utils.images import convert_compress
from app.utils.selenium import driver
from app.Models.Screenshot import Screenshot
from app.Models.JopRecordStatus import JopRecordStatus
from app.Models.JobRecord import JobRecord
from app.Models.Job import Job
from flask import jsonify, Response
from app.functions import functions
from app.Models.Service import Service
from selenium.webdriver.common.by import By



class Job_record_controller:
    
    def create(self, job_id):
        print('job_record')
        initialTime = 0
        job = ''
        try:
            job = Job.find_by_id(job_id)
            if job is None:
                return Response('{"error":"job not exist"}', status=404, mimetype='application/json')
        except Exception:
            return Response('{"error":"server error in job"}', status=404, mimetype='application/json')

        if not job.action == 'XPATH':
            initialTime = time.time()
            response = functions[job.action](job.url)
            if response:
                finishedTime = time.time()
                getstatus = JopRecordStatus.find_by_name('online')
                job_record = JobRecord(**{
                    'job_id': job.id,
                    'status_id': getstatus.id,
                    'time_spent_in_sec': finishedTime - initialTime,
                }).save()
                return jsonify(
                    id=job_record.id,
                    time_spent_in_sec=job_record.time_spent_in_sec,
                    service_id=job_record.id,
                    status_id=job_record.status_id,
                    createdAt=job_record.created_at
                )
            else:
                finishedTime = time.time()
                getstatus = JopRecordStatus.find_by_name('offline')
                JobRecord(**{
                    'job_id': job.id,
                    'status_id': getstatus.id,
                    'time_spent_in_sec': finishedTime - initialTime,
                }).save()
                return Response('{"error":"job {job.service.name} offline"}', status=500, mimetype='application/json')

        try:
            image_name = f'{job.service.service_group.name}_{job.service.name}_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
            image_path = f"{ROOT_PATH}/image_records/{image_name}.png"
            initialTime = time.time()

            driver.get(f'{job.url}')
            time.sleep(5)
            driver.get_screenshot_as_file(image_path)
            convert_compress(image_path)
            driver.find_element(By.XPATH, job.action_value).is_displayed()
            finishedTime = time.time()
            getstatus = JopRecordStatus.find_by_name('online')
            job_record = JobRecord(**{
                'job_id': job.id,
                'status_id': getstatus.id,
                'time_spent_in_sec': finishedTime - initialTime,
            }).save()
            image = {
                "url": image_path,
                "mime_type": "images/png",
                "job_record_id": job_record.id
            }
            Screenshot(**image).save()

            print(finishedTime - initialTime)
            return jsonify(
                id=job_record.id,
                time_spent_in_sec=job_record.time_spent_in_sec,
                service_id=job_record.id,
                status_id=job_record.status_id,
                createdAt=job_record.created_at
            )
        except:
            finishedTime = time.time()
            getstatus = JopRecordStatus.find_by_name('offline')
            job_record =JobRecord(**{
                'job_id': job.id,
                'status_id': getstatus.id,
                'time_spent_in_sec': finishedTime - initialTime,
            }).save()
            return jsonify(
                id=job_record.id,
                time_spent_in_sec=job_record.time_spent_in_sec,
                service_id=job_record.id,
                status_id=job_record.status_id,
                createdAt=job_record.created_at
            )

    def get_job_records_by_service(self,service_id):
        jobs_records_response = JobRecord.query.join(Job).filter(Job.service_id == service_id ).order_by(JobRecord.created_at.desc())
        service = Service.find_by_id(service_id)
        jobs_records = []
        for job_record in jobs_records_response:
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
            jobs_records.append(current_job_record)
        
        return {"jobs_records":jobs_records,"name":service.name}

    def __create_object_job_record_if_name_equal_service_name(self,job_record,jobs_record_service):
        
        count_online = 0
        count_offline = 0
        if job_record.created_at > jobs_record_service['last_updated']:
            date_time_format = job_record.created_at.strftime('Última atualização %d de %B de %Y %H:%M')
            jobs_record_service['last_updated'] = job_record.created_at
            if (jobs_record_service['status'] == 'online') & (job_record.status.value == 'offline'):
                count_online -=1
                count_offline+=1
            if (jobs_record_service['status'] == 'offline') & (job_record.status.value == 'online'):
                count_online +=1
                count_offline -=1
            jobs_record_service['status'] = job_record.status.value
            jobs_record_service['date_time_format'] = date_time_format
        return  {
               'job_record':{
                'id': job_record.id,
                'status': job_record.status.value,
                'time_spent_in_sec': job_record.time_spent_in_sec,
                'job': {
                    "id": job_record.job.id,
                    "order": job_record.job.order,
                    "url": job_record.job.url,
                    "action": job_record.job.action,
                    "action_value": job_record.job.action_value,
                }
               },
               "count_offline":count_offline,"count_online":count_online
            }
       
    def all(self):
        print("==================== CAPTURANDO TODOS OS JOB RECORDS ====================")
        jobs_records = JobRecord.query.order_by(JobRecord.id).all()
        jobs_record_array =[]
        
        count_online = 0
        count_offline = 0
       
        for job_record in jobs_records:
            index =0
            value = True
            while value:
                if index +1 <= jobs_record_array.__len__() and job_record.job.service.service_group.id == jobs_record_array[index]["id"]:
                    exist_service = False
                    for service in jobs_record_array[index]["services"]:
                        if service['name'] == job_record.job.service.name:
                            create_record_to_jobs = self.__create_object_job_record_if_name_equal_service_name(job_record,service)
                            count_offline +=create_record_to_jobs['count_offline']
                            count_online +=create_record_to_jobs['count_online']
                            service['jobs'].append(create_record_to_jobs['job_record'])
                            if not service['status'] == create_record_to_jobs['job_record']['status']:
                                service['status'] = 'warning'
                            exist_service = True
                    if not exist_service:
                        if job_record.status.value == 'online':
                            count_online += 1
                        else:
                            count_offline +=1
                        date_time_format = job_record.created_at.strftime('Última atualização %d de %B de %Y %H:%M')
                        jobs_record_array[index]['services'].append({
                            "id": job_record.job.service.id,
                            "name": job_record.job.service.name,
                            "status":job_record.status.value,
                            "last_updated":job_record.created_at,
                            "date_time_format":date_time_format,
                            "jobs": [
                                {
                                    'id': job_record.id,
                                    'status': job_record.status.value,
                                    'time_spent_in_sec': job_record.time_spent_in_sec,
                                    'job': {
                                        "id": job_record.job.id,
                                        "order": job_record.job.order,
                                        "url": job_record.job.url,
                                        "action": job_record.job.action,
                                        "action_value": job_record.job.action_value,
                                    }
                                }
                            ]
                        })
                    value = False
                elif index == jobs_record_array.__len__():
                    # if not index == 0:
                    #     print("index",index)
                    #     print("job_record",job_record.job.service.service_group.id)
                    #     print("id",jobs_record_array[index]["id"])
                    #     print(job_record.job.service.service_group.id == jobs_record_array[index]["id"])
                    if job_record.status.value == 'online':
                        count_online += 1
                    else:
                        count_offline +=1
                    jobs_record_array.append({
                        "service_group": job_record.job.service.service_group.name,
                        "id": job_record.job.service.service_group.id,
                        "services":
                        [
                            {
                                "id": job_record.job.service.id,
                                "name": job_record.job.service.name,
                                "status":job_record.status.value,
                                "last_updated":job_record.created_at,
                                "jobs": [
                                    {
                                        'id': job_record.id,
                                        'status': job_record.status.value,
                                        'time_spent_in_sec': job_record.time_spent_in_sec,
                                        'job': {
                                            "id": job_record.job.id,
                                            "order": job_record.job.order,
                                            "url": job_record.job.url,
                                            "action": job_record.job.action,
                                            "action_value": job_record.job.action_value,
                                        }
                                    }
                                ]
                            }
                        ]
                    })   
                    value = False

                index = index +1
         
                
        
        
        print("==================== CAPTURANDO TODOS OS JOB RECORDS - END ====================")
        return {"jobs_record_array":jobs_record_array,"count_online":count_online,"count_offline":count_offline}
        # return jobs_record_array