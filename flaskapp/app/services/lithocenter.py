from datetime import datetime
import os

from app.settings import ROOT_PATH
from app.utils.images import convert_compress
# from app.utils.selenium import driver
from app.services.db import db
from app.Models.Service import Service
from app.Models.StatusImage import StatusImage
from app.Models.Status import Status
from app.Models.StatusRecord import StatusRecord

from selenium.webdriver.common.by import By
from app.services.verifyFrontendStatus import verifyFrontendStatus


SERVICE_NAME = "LITHOCENTER"


def check_frontend():
    print("44")
    verifyFrontendStatus(f'https://lithocenterhospitaldia.com',"//div[@class='phone']/a[@class='number']",'LITHOCENTER')
    print("passou")
    # SUBSERVICE_NAME = "FRONTEND"
    # URL = "//div[@class='phone']/a[@class='number']"
    # image_name = f'{SERVICE_NAME}_{SUBSERVICE_NAME}_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
    # image_path = f'{ROOT_PATH}/image_records/{image_name}.png'

    # driver.get(URL)
    # # Capture screenshot
    # driver.get_screenshot_as_file(image_path)
    # # Compress screenshot image file
    # convert_compress(image_path)
    # # Verify if a MUST HAVE element exists when loading frontend
    # find_element = driver.find_element(By.XPATH,
    #                                    ).is_displayed()
    # TODO Add record to sqlite database
    # newStatus = StatusRecord(username="lucas",email="lucas@gmail.com")
    # newStatus = Service(username="lucas",email="lucas@gmail.com")
    # db.session.add(newStatus)
    # db.session.commit()

    
    return 
