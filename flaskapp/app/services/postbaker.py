from datetime import datetime
import os

from app.settings import ROOT_PATH
from app.utils.images import convert_compress
from app.utils.selenium import driver

from selenium.webdriver.common.by import By
from app.services.verifyFrontendStatus import verifyFrontendStatus


def check_frontend():
    verifyFrontendStatus(f'https://app.postbaker.com.br/login/',"//fieldset/input[@type='email']",'POSTBAKER')
    
    # SUBSERVICE_NAME = 'FRONTEND'
    # image_name = f'{SERVICE_NAME}_{SUBSERVICE_NAME}_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
    # image_path =f'{ROOT_PATH}/image_records/{image_name}.png'
    # driver.get(URL)
    # driver.get_screenshot_as_file(image_path)
    # convert_compress(image_path)

    return True