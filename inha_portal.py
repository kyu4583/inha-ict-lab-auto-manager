import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from chrome_driver_updater import setup_chrome_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 드라이버 설치 및 경로 설정
driver_path = setup_chrome_driver()

# 크롬 옵션을 설정합니다.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('window-size=1920x1080')

# 웹 드라이버에 service와 options 값을 전달합니다.
s = Service(driver_path)
driver = webdriver.Chrome(service=s, options=chrome_options)

# 웹 페이지 열기
portal_url = "https://portal.inha.ac.kr"
driver.get(portal_url)

# 아이디와 비밀번호 입력 필드 찾기
user_id_input = driver.find_element(By.ID, "userId")
password_input = driver.find_element(By.ID, "passwd")

# 아이디와 비밀번호 입력
user_id_input.send_keys(os.getenv("PORTAL_ID"))
password_input.send_keys(os.getenv("PORTAL_PW"))

# 로그인 버튼 클릭
login_button = driver.find_element(By.XPATH, "//input[@class='ep-btnid']")
login_button.click()

ins_url = "https://ins2.inha.ac.kr/ins/"
driver.get(ins_url)

frame = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, "INSMain"))
)

frame = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, "Left"))
)

# '정보통신' 메뉴 클릭을 위한 XPath 사용 (실제 XPath로 변경 필요)
info_comm_link = driver.find_element(By.ID, 'JB_03006')
info_comm_link.click()

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="SideMenu"]/ul/li[11]/ul/li/a'))
)
button.click()

# 메인 컨텐츠로 컨텍스트 전환
driver.switch_to.default_content()

# 두 번째 프레임으로 컨텍스트 전환
frame = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, "INSMain"))
)

frame = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, "Main"))
)

frame = WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it((By.ID, "ifTab"))
)

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/form/table/tbody/tr[1]/td[1]/img'))
)
button.click()

button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div/table/tbody/tr[2]/td[1]/a'))
)
button.click()

lab_select_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ddlLabList"))
)

# Select 객체 생성
lab_select = Select(lab_select_element)

# 원하는 실습실 선택
# value 값으로 선택
lab_select.select_by_value("60주년-808")


# 조회 버튼 찾기 및 클릭
search_button = driver.find_element(By.ID, "btnSearch")
search_button.click()


input("Press Enter to quit")
driver.quit()