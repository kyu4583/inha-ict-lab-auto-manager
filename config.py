import logging
import os
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

feedback_logger = logging.getLogger('feedback_logger')
console_logger = logging.getLogger('console_logger')

chrome_version_logged = False

def get_default_portal_id():
    return os.getenv("INHA_PORTAL_ID")

def get_default_portal_pw():
    return os.getenv("INHA_PORTAL_PW")

def get_max_web_drivers():
    return int(os.getenv('MAX_WEB_DRIVERS', '5'))

if get_default_portal_id() and get_default_portal_pw():
    console_logger.info("Successfully loaded default portal ID and password from environment variables.")
else:
    console_logger.warning("Failed to load default portal ID or password from environment variables.")

def create_web_driver():
    # 고유 ID 생성
    driver_id = uuid.uuid4()
    console_logger.debug(f"WebDriver instance {driver_id} is being created.")

    # 크롬 옵션 설정
    chrome_options = webdriver.ChromeOptions()
    headless_mode = os.getenv('HEADLESS_MODE', 'True') == 'True'
    if headless_mode:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
    if os.name != 'nt':
        chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('window-size=1920x1080')

    # 웹 드라이버 생성
    s = Service()
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.id = driver_id

    # 크롬 버전 및 크롬 드라이버 버전 로그 출력 (최초 1회만)
    global chrome_version_logged
    if not chrome_version_logged:
        log_version_info(driver)
        chrome_version_logged = True

    return driver

def log_version_info(driver):
    browser_version = driver.capabilities['browserVersion']
    driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    browser_path = driver.capabilities['chrome']['userDataDir']
    driver_path = driver.service.path
    console_logger.info(f"Chrome browser version: {browser_version}, ChromeDriver version: {driver_version}")
    console_logger.info(f"Chrome browser path: {browser_path}, ChromeDriver path: {driver_path}")

def quit_web_driver(driver):
    console_logger.debug(f"WebDriver instance {driver.id} is being destroyed.")
    driver.quit()