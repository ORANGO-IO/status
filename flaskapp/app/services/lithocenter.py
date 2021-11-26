from datetime import datetime
import os

from app.settings import ROOT_PATH
from app.utils.images import convert_compress
from app.utils.selenium import driver

from selenium.webdriver.common.by import By


SERVICE_NAME = "LITHOCENTER"


def check_frontend():
    SUBSERVICE_NAME = "FRONTEND"
    URL = f'https://lithocenterhospitaldia.com'
    image_name = f'{SERVICE_NAME}_{SUBSERVICE_NAME}_{datetime.now().strftime("%Y_%m_%d__%H_%M_%S")}'
    image_path = f'{ROOT_PATH}/image_records/{image_name}.png'

    driver.get(URL)
    driver.get_screenshot_as_file(image_path)
    convert_compress(image_path)

    return driver.find_element(By.XPATH,
                               "//div[@class='phone']/a[@class='number']").is_displayed()
