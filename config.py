import os
import uuid  # UUID 모듈 추가
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
            print(f"Driver instance {Driver._instance.id} is being reset.")  # 소멸 로그
            Driver._instance.quit()
        Driver._instance = Driver().driver

    def __init__(self):
        # 고유 ID 생성
        self.id = uuid.uuid4()
        print(f"Driver instance {self.id} is being created.")  # 생성 로그

        # 크롬 옵션 설정
        chrome_options = webdriver.ChromeOptions()

        # 환경 변수 읽기
        headless_mode = os.getenv('HEADLESS_MODE', 'True') == 'True'

        if headless_mode:
            # 무헤드 모드 추가
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 안 함
            chrome_options.add_argument("--disable-gpu")  # GPU 가속 비활성화

        chrome_options.add_argument('window-size=1920x1080')

        # 웹 드라이버에 service와 options 값 전달
        s = Service()
        self.driver = webdriver.Chrome(service=s, options=chrome_options)
        self.driver.id = self.id  # 드라이버에 ID 할당

        # 크롬 버전 및 크롬 드라이버 버전 로그 출력
        self.print_version_info()

    def print_version_info(self):
        # 크롬 브라우저 버전
        browser_version = self.driver.capabilities['browserVersion']
        # 크롬 드라이버 버전
        driver_version = self.driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        print(f"Chrome browser version: {browser_version}")
        print(f"ChromeDriver version: {driver_version}")

    def __del__(self):
        print(f"Driver instance {self.id} is being destroyed.")  # 소멸 로그
