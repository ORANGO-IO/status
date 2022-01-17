from datetime import datetime
import time

from app.settings import ROOT_PATH
from app.utils.images import convert_compress
from app.utils.selenium import driver
from app.Models.Screenshot import Screenshot
from app.Models.JopRecordStatus import JopRecordStatus
from app.Models.JobRecord import JobRecord
from app.Models.Job import Job
from flask import jsonify,Response

from selenium.webdriver.common.by import By

class Job_record_controller:
    def create(self,job_id):
        print('job_record')

        try:
            job = Job.find_by_id(job_id)
            if job is None:
                return Response('{"error":"job not exist"}', status=404, mimetype='application/json')
            image_name = f'{job.service.name}_SUBSERVICE_NAME_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
            image_path = f"{ROOT_PATH}/image_records/{image_name}.png"
            initialTime =  time.time()
            
            driver.get(f'{job.url}')
            driver.get_screenshot_as_file(image_path)
            convert_compress(image_path)
            driver.find_element(By.XPATH,job.action_value).is_displayed()
            
            finishedTime = time.time()
            getstatus = JopRecordStatus.find_by_name('online')
            job_record = JobRecord(**{
                'job_id':job.id,
                'status_id':getstatus.id,
                'time_spent_in_sec': finishedTime -initialTime,
                }).save()
            image = {
                "url":image_path,
                "mime_type":"images/png",
                "job_record_id":job_record.id
                }
            Screenshot(**image).save()

            print( finishedTime -initialTime)
            return jsonify(
                id=job_record.id,
                time_spent_in_sec=job_record.time_spent_in_sec,
                service_id=job_record.id,
                status_id=job_record.status_id,
                createdAt=job_record.created_at
            )
        except:
            # print("getstatus.id")
            # getService = Service.find_by_name(serviceName)
            # getstatus = JopRecordStatus.find_by_name('offline')
            # JobRecord(**{
            # 'service_id':getService.id,
            # 'status_id':getstatus.id,
            # }).save()
            return Response('{"error":"server error"}', status=500, mimetype='application/json')



