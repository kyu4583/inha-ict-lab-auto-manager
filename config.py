from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from chrome_driver_updater import setup_chrome_driver

class Driver:
    _instance = None

    @staticmethod
    def get_instance():
        if Driver._instance is None:
            Driver._instance = Driver().driver
        return Driver._instance

    @staticmethod
    def reset_instance():
        Driver._instance.quit()
        Driver._instance = Driver().driver

    def __init__(self):
        # 드라이버 설치 및 경로 설정
        driver_path = setup_chrome_driver()

        # 크롬 옵션을 설정합니다.
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('window-size=1920x1080')

        # 웹 드라이버에 service와 options 값을 전달합니다.
        s = Service(driver_path)
        self.driver = webdriver.Chrome(service=s, options=chrome_options)

