import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class Driver:
    _instance = None

    @staticmethod
    def get_instance():
        if Driver._instance is None:
            Driver._instance = Driver().driver
        return Driver._instance

    @staticmethod
    def reset_instance():
        if Driver._instance:
            Driver._instance.quit()
        Driver._instance = Driver().driver

    def __init__(self):

        # 크롬 옵션 설정
        chrome_options = webdriver.ChromeOptions()

        # 환경 변수 읽기
        headless_mode = os.getenv('HEADLESS_MODE', 'True') == 'True'

        if headless_mode:
            # 무헤드 모드 추가
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")  # sandbox 비활성화
            chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 안 함
            chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화

        chrome_options.add_argument('window-size=1920x1080')

        # 웹 드라이버에 service와 options 값 전달
        s = Service()
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
