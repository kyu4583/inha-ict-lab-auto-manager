import os
import chromedriver_autoinstaller

def setup_chrome_driver():
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    # chrome driver의 버전 정보를 가져옵니다.

    current_path = os.getcwd()
    # 현재 파일의 경로를 가져옵니다.

    driver_path = f'{current_path}/{chrome_ver}/chromedriver.exe'
    # 현재 폴더 안에 chrome_ver(예를 들어 101.2) 폴더를 만들어 이 안에 chromedriver.exe를 다운 받도록 합니다. - 경로 지정

    if not os.path.exists(driver_path):
        chromedriver_autoinstaller.install(True)
        print(f"Chrome driver(ver: {chrome_ver}) is installed at {driver_path}")
    return driver_path
    # 최신 버전이 아니면(해당 버전의 폴더가 없으면) 다운받습니다.