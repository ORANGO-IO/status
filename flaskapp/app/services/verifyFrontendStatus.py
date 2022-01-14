from datetime import datetime
import os

from app.settings import ROOT_PATH
from app.utils.images import convert_compress
from app.utils.selenium import driver
from app.services.db import db
from app.Models.Service import Service
from app.Models.Screenshot import Screenshot
from app.Models.JopRecordStatus import JopRecordStatus
from app.Models.JobRecord import JobRecord

from selenium.webdriver.common.by import By

def verifyFrontendStatus(url,xpath,serviceName):
    SUBSERVICE_NAME = "FRONTEND"
    image_name = f'{serviceName}_{SUBSERVICE_NAME}_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
    image_path = f'{ROOT_PATH}/image_records/{image_name}.png'
    try:
        driver.get(url)
        driver.get_screenshot_as_file(image_path)
        convert_compress(image_path)
        find_element = driver.find_element(By.XPATH,xpath).is_displayed()
        # TODO Add record to sqlite database
        print(find_element)
        image = {
            "url":image_path,
            "mime_type":"images/png"
            }
        newImage = Screenshot(**image).save()
        getService = Service.find_by_name(serviceName)
        if find_element == False:
            getstatus = JopRecordStatus.find_by_name('off')
            print(getstatus.id)
            JobRecord(**{
            'service_id':getService.id,
            'status_id':getstatus.id,
            'image_id': newImage.id,
            }).save()
            return

        getstatus = JopRecordStatus.find_by_name('on')
        print(getstatus.id)
        JobRecord(**{
        'service_id':getService.id,
        'status_id':getstatus.id,
        'image_id': newImage.id,
        }).save()
        return 
    except:
        print("getstatus.id")
        getService = Service.find_by_name(serviceName)
        getstatus = JopRecordStatus.find_by_name('off')
        JobRecord(**{
        'service_id':getService.id,
        'status_id':getstatus.id,
        }).save()
        return

        # getstatus = Status.find_by_username('on')
        # print(getstatus.id)
        # JobRecord(**{
        # 'service_id':getService.id,
        # 'status_id':getstatus.id,
        # 'image_id': newImage.id,
        # }).save()

