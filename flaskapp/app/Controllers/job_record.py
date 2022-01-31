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
        except:
            return Response('{"error":"server error in job"}', status=404, mimetype='application/json')

        if not job.action == 'XPATH':
            initialTime = time.time()
            response = functions[job.action]()
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
            image_name = f'{job.service.name}_SUBSERVICE_NAME_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
            image_path = f"{ROOT_PATH}/image_records/{image_name}.png"
            initialTime = time.time()

            driver.get(f'{job.url}')
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
            JobRecord(**{
                'job_id': job.id,
                'status_id': getstatus.id,
                'time_spent_in_sec': finishedTime - initialTime,
            }).save()
            return Response('{"error":"job {job.service.name} offline"}', status=500, mimetype='application/json')

    def all(self):
        print("==================== CAPTURANDO TODOS OS JOB RECORDS ====================")
        jobs_records = JobRecord.query.order_by(JobRecord.id).all()
        jobs_record_array = []
        print(jobs_records)
        for job_record in jobs_records:
            if jobs_record_array.__len__() == 0:
                jobs_record_array.append(dict(**{
                    "service_group": job_record.job.service.service_group.name,
                    "services": list([
                        {
                            "id": job_record.job.service.id,
                            "name": job_record.job.service.name,
                            "jobs": list([
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
                            ])

                        }
                    ])

                }))
            else:
                for index, x in enumerate(jobs_record_array):
                    print("x")
                    print(x)
                    if x["service_group"] == job_record.job.service.service_group.name:
                        exist_service = False
                        for y in x["services"]:
                            if y['name'] == job_record.job.service.name:
                                print("type(y['jobs'])")
                                print(type(y['jobs']))
                                print("type(y)")
                                print(type(y))
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
                                break
                        if not exist_service:
                            x['services'].append({
                                "id": job_record.job.service.id,
                                "name": job_record.job.service.name,
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
                        break
                    elif index + 1 == jobs_record_array.__len__():
                        jobs_record_array.append({
                            "service_group": job_record.job.service.service_group.name,
                            "services":
                            [
                                {
                                    "id": job_record.job.service.id,
                                    "name": job_record.job.service.name,
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
        print(jobs_record_array)
        print("==================== CAPTURANDO TODOS OS JOB RECORDS - END ====================")
        return jsonify(jobs_record_array)
        # except:
        #     return Response('{"error":"server error"}', status=500, mimetype='application/json')
