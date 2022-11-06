from app.functions import functions
from app.Models.Job import Job
from datetime import datetime
import time
from app.settings import ROOT_PATH
from app.utils.images import convert_compress
from app.utils.selenium import driver
from app.Models.Screenshot import Screenshot
from app.Models.JopRecordStatus import JopRecordStatus
from selenium.webdriver.common.by import By
from app.Models.JobRecord import JobRecord
from flask import jsonify

def record_job_default_strategy(job):
    initialTime = 0
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
        job_record =JobRecord(**{
            'job_id': job.id,
            'status_id': getstatus.id,
            'time_spent_in_sec': finishedTime - initialTime,
        }).save()
        return job_record

def record_job_xpath_strategy(job):
    initialTime = 0
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

        return job_record

    except:
        finishedTime = time.time()
        getstatus = JopRecordStatus.find_by_name('offline')
        job_record =JobRecord(**{
            'job_id': job.id,
            'status_id': getstatus.id,
            'time_spent_in_sec': finishedTime - initialTime,
        }).save()
        return job_record

strategies = {
    'XPATH': record_job_xpath_strategy,
    'default': record_job_default_strategy,
}

def record_job_strategy(job:Job):
    strategy = None
    if job.action in strategies:
        strategy = strategies[job.action]
    else:
        strategy = strategies['default']
    return strategy(job)
      

