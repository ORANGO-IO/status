from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

binary = '/usr/bin/firefox'
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.log.level = "trace"
options.binary = binary
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True

driver = webdriver.Firefox(
    firefox_options=options, capabilities=cap, executable_path="/usr/local/bin/geckodriver")
print('Acessando a página', flush=True)

wait = WebDriverWait(driver, 10)
print(driver.execute_script("return document.readyState"), flush=True)
element = wait.until(lambda driver: driver.execute_script(
    'return document.readyState') == 'complete')