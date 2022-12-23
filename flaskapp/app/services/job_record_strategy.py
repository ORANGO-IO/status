from app.services.job_record_functions import job_record_functions
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
import re

def record_job_default_strategy(job):
    initialTime = 0
    initialTime = time.time()        
    response = job_record_functions[job.action](job.url)
    if response:
        finishedTime = time.time()
        getstatus = JopRecordStatus.find_by_name('online')
        job_record = JobRecord(**{
            'job_id': job.id,
            'status_id': getstatus.id,
            'time_spent_in_sec': finishedTime - initialTime,
        }).save()
        return job_record
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
        service_group_name_whitout_spaec = re.sub(' +', ' ', job.service.service_group.name)
        service_name_whitout_spaec = re.sub(' +', ' ', job.service.name)
        image_name = f'{service_group_name_whitout_spaec}_{service_name_whitout_spaec}_{datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}'
        image_path_save = f"{ROOT_PATH}/static/image_records/{image_name}.png"
        image_path = f"static/image_records/{image_name}.jpg"
        initialTime = time.time()

        driver.get(f'{job.url}')
        time.sleep(10)
        driver.get_screenshot_as_file(image_path_save)
        convert_compress(image_path_save)
        driver.find_element(By.XPATH, job.action_value).is_displayed()
        finishedTime = time.time()
        getstatus = JopRecordStatus.find_by_name('online')
        job_record = JobRecord(**{
            'job_id': job.id,
            'status_id': getstatus.id,
            'time_spent_in_sec': finishedTime - initialTime,
            'created_at':datetime.now()
        }).save()
        image = {
            "url": image_path,
            "mime_type": "images/jpg",
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
            'created_at':datetime.now()
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
      

