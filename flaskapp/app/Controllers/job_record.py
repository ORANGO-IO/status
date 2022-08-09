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
            # return Response('{"error":"job {job.service.name} offline"}', status=500, mimetype='application/json')

    def all(self):
        print("==================== CAPTURANDO TODOS OS JOB RECORDS ====================")
        jobs_records = JobRecord.query.order_by(JobRecord.id).all()
        jobs_record_array =[]
        
        count_online = 0
        count_offline = 0
        for job_record in jobs_records:
            if jobs_record_array.__len__() == 0:
                date_time_format = job_record.created_at.strftime('Última atualização %d de %B de %Y %H:%M')
                if job_record.status.value == 'online':
                    count_online += 1
                else:
                    count_offline +=1
                jobs_record_array.append({
                    "service_group": job_record.job.service.service_group.name,
                    "services": [
                        {
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

                        }
                    ]

                })

            else:
                for index, x in enumerate(jobs_record_array):
                    if job_record.job.service.service_group.name == x["service_group"]:
                        exist_service = False
                        for y in x["services"]:
                            if y['name'] == job_record.job.service.name:
                                if(job_record.created_at > y['last_updated']):
                                    date_time_format = job_record.created_at.strftime('Última atualização %d de %B de %Y %H:%M')
                                    y['last_updated'] = job_record.created_at
                                    if y['status'] == 'online' & job_record.status.value == 'offline':
                                        count_online -=1
                                        count_offline+=1
                                    if y['status'] == 'offline' & job_record.status.value == 'online':
                                        count_online +=1
                                        count_offline -=1
                                    y['status'] = job_record.status.value
                                    y['date_time_format'] = date_time_format
                                
                                y['jobs'].append(
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
                                )
                                exist_service = True
                        if not exist_service:
                            if job_record.status.value == 'online':
                                count_online += 1
                            else:
                                count_offline +=1
                            date_time_format = job_record.created_at.strftime('Última atualização %d de %B de %Y %H:%M')
                            x['services'].append({
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
                    if index + 1 == jobs_record_array.__len__():
                        if job_record.status.value == 'online':
                            count_online += 1
                        else:
                            count_offline +=1
                        jobs_record_array.append({
                            "service_group": job_record.job.service.service_group.name,
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
            
        
        
        print("==================== CAPTURANDO TODOS OS JOB RECORDS - END ====================")
        return {"jobs_record_array":jobs_record_array,"count_online":count_online,"count_offline":count_offline}
        # return jobs_record_array