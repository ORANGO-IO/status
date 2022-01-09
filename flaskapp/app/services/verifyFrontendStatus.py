from datetime import datetime
import os

from app.settings import ROOT_PATH
from app.utils.images import convert_compress
from app.utils.selenium import driver
from app.services.db import db
from app.Models.Service import Service
from app.Models.StatusImage import StatusImage
from app.Models.Status import Status
from app.Models.StatusRecord import StatusRecord

from selenium.webdriver.common.by import By


SERVICE_NAME = "LITHOCENTER"


def verifyFrontendStatus(url,xpath,serviceName):
    SUBSERVICE_NAME = "FRONTEND"
    image_name = f'{SERVICE_NAME}_{SUBSERVICE_NAME}_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
    image_path = f'{ROOT_PATH}/image_records/{image_name}.png'

    print("driver")
    driver.get(url)
    print('driver')
    print(driver)
    
    # Capture screenshot
    driver.get_screenshot_as_file(image_path)
    # Compress screenshot image file
    convert_compress(image_path)
    print(image_path)
    # Verify if a MUST HAVE element exists when loading frontend
    # newImage = StatusImage(url=image_path,mime_type="teste")
    find_element = driver.find_element(By.XPATH,xpath).is_displayed()
    # TODO Add record to sqlite database
    print(find_element)
    # if(find_element)


    # newStatus = Service(username="lucas",email="lucas@gmail.com")
    # newStatus = StatusRecord(username="lucas",email="lucas@gmail.com")
    # db.session.add(newStatus)
    # db.session.commit()

    return 
