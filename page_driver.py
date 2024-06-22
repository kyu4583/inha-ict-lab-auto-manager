import os
import logging
import time

from selenium.common import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import calendar_manager as cm
import config
import datetime

feedback_logger = logging.getLogger('feedback_logger')
console_logger = logging.getLogger('console_logger')

# 환경 변수에서 ID와 PW 불러오기
default_portal_id = os.getenv("INHA_PORTAL_ID")
default_portal_pw = os.getenv("INHA_PORTAL_PW")

# ID와 PW가 제대로 불러와졌는지 확인하고 로그 출력
if default_portal_id and default_portal_pw:
    console_logger.info("Successfully loaded default portal ID and password from environment variables.")
else:
    console_logger.warning("Failed to load default portal ID or password from environment variables.")


def get_driver():
    return driver


def reset_driver():
    config.Driver.reset_instance()
    global driver
    driver = config.Driver.get_instance()

def logout_and_reset_driver():
    try:
        log_out()
    except Exception as e:
        pass
    reset_driver()

def open_url(url):
    time.sleep(0.01)
    driver.get(url)


def open_portal():
    feedback_logger.info("포털 접속중..")
    open_url("https://portal.inha.ac.kr")
    feedback_logger.info("포털 접속 완료.")


def log_in(id=default_portal_id, pw=default_portal_pw):
    feedback_logger.info("로그인 시도 중...")
    # WebDriverWait를 사용해 요소가 로드될 때까지 대기
    user_id_input = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "userId"))
    )
    password_input = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "passwd"))
    )

    # 아이디, 비번 입력
    user_id_input.send_keys(id)
    password_input.send_keys(pw)

    # 로그인 버튼 클릭
    login_button = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class='ep-btnid']"))
    )
    login_button.click()
    feedback_logger.info("로그인 완료.")


def log_out():
    feedback_logger.info("로그아웃 시도 중...")
    open_portal()

    # 로그아웃 버튼 클릭
    logout_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"gnb\"]/ul/li[5]/a"))
    )
    logout_button.click()
    feedback_logger.info("로그아웃 완료.")


def open_ins_from_portal_after_login():
    feedback_logger.info("학사행정 페이지로 이동 중...")
    open_url("https://ins2.inha.ac.kr/ins/")
    feedback_logger.info("학사행정 페이지 접속 완료.")


def start_and_enter_lab_manage(id=None, pw=None):
    open_portal()
    if id is None:
        log_in()
    else:
        log_in(id, pw)
    open_ins_from_portal_after_login()
    open_lab_manage_from_ins()


def handle_alert_or_timeout_and_retry(action, max_retries=15):
    retries = 0
    while retries < max_retries:
        try:
            logout_and_reset_driver()
            action()
            return
        except UnexpectedAlertPresentException as e:
            console_logger.warning(f"UnexpectedAlertPresentException: {e}. Retrying {retries + 1}/{max_retries}")
            retries += 1
        except TimeoutException as e:
            console_logger.warning(f"TimeoutException: {e}. Retrying {retries + 1}/{max_retries}")
            retries += 1
        except Exception as e:
            console_logger.error(f"Exception: {e}. Retrying {retries + 1}/{max_retries}")
            retries += 1
    console_logger.error("Max retries exceeded")
    raise Exception("Max retries exceeded")


def start_and_enter_lab_manage_handling_except(id=None, pw=None):
    handle_alert_or_timeout_and_retry(lambda: start_and_enter_lab_manage(id, pw))


def frame_insMain():
    switch_default_content()
    WebDriverWait(driver, 4).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "INSMain"))
    )


def frame_insMain_main():
    switch_default_content()
    frame_insMain()
    WebDriverWait(driver, 4).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "Main"))
    )


def frame_insMain_left():
    switch_default_content()
    frame_insMain()
    WebDriverWait(driver, 4).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "Left"))
    )


def frame_insMain_main_ifTab():
    switch_default_content()
    frame_insMain_main()
    WebDriverWait(driver, 4).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "ifTab"))
    )


def open_lab_manage_from_ins():
    feedback_logger.debug("실습실 관리 탭 이동 중...")
    switch_default_content()
    frame_insMain()
    frame_insMain_main()
    frame_insMain_left()

    # '정보통신' 메뉴 클릭을 위한 XPath 사용
    info_comm_link = driver.find_element(By.ID, 'JB_03006')
    info_comm_link.click()

    button = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="SideMenu"]/ul/li[12]/ul/li/a'))
    )
    button.click()
    feedback_logger.debug("실습실 관리 탭 이동 완료.")


def switch_default_content():
    # 메인 컨텐츠로 컨텍스트 전환
    driver.switch_to.default_content()


def lab_manage_select_date(day=None, month=None, year=None):
    feedback_logger.debug("날짜 선택 중...")
    today = datetime.date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    if day is None:
        day = today.day

    frame_insMain_main_ifTab()

    button = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/form/table/tbody/tr[1]/td[1]/img'))
    )
    button.click()

    cm.add_monthly_calendar(month, year)
    coordinates = cm.calendar_data[year][month]['coordinates']

    year_select_element = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[1]/div/select[1]')
        )
    )
    year_select = Select(year_select_element)
    year_select.select_by_value(str(year))

    month_select_element = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[1]/div/select[2]')
        )
    )
    month_select = Select(month_select_element)
    month_select.select_by_value(str(month - 1))

    day_button = WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable(
            (By.XPATH, f'/html/body/div/table/tbody/tr[{coordinates[day][0]}]/td[{coordinates[day][1]}]/a'))
    )
    day_button.click()
    feedback_logger.debug("날짜 선택 완료.")


def lab_manage_select_lab(lab):
    feedback_logger.debug("실습실 선택 중...")
    frame_insMain_main_ifTab()

    # 실습실 선택
    lab_select_element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "ddlLabList"))
    )
    lab_select = Select(lab_select_element)
    lab_select.select_by_value(lab.value)
    feedback_logger.debug("실습실 선택 완료.")


def lab_manage_search():
    frame_insMain_main_ifTab()

    # 조회 버튼 클릭
    search_button = driver.find_element(By.ID, "btnSearch")
    search_button.click()


def lab_manage_select_time(time):
    feedback_logger.debug(f"{time}교시 선택 중...")
    frame_insMain_main_ifTab()

    # 시간 선택
    time_select_element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "ddlTimeList"))
    )
    time_select = Select(time_select_element)
    time_select.select_by_value(str(time))
    feedback_logger.debug(f"{time}교시 선택 완료.")


def lab_manage_insert_user_number(num=0):
    feedback_logger.debug(f"사용자 수 {num} 입력 중...")
    user_number_input = driver.find_element(By.ID, "txtInwon")

    user_number_input.send_keys(num)

    user_number_select_element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "ddlUseGubun"))
    )
    user_number_select = Select(user_number_select_element)
    user_number_select.select_by_value("0")

    # 저장 버튼 클릭
    save_button = driver.find_element(By.NAME, "btnSave")
    save_button.click()

    # 팝업 확인 * 2번
    send_popup_OK_twice()
    feedback_logger.debug(f"사용자 수 {num} 입력 완료.")


def lab_manage_insert_lecture_schedule():
    feedback_logger.debug("강의 일정 입력 시작.")
    user_number_select_element = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "ddlUseGubun"))
    )
    user_number_select = Select(user_number_select_element)
    user_number_select.select_by_value("01")

    save_button = driver.find_element(By.NAME, "btnSave")
    save_button.click()

    send_popup_OK_twice()
    feedback_logger.debug("강의 일정 입력 완료.")

def send_popup_OK_twice():
    feedback_logger.debug("팝업 확인 작업 시작.")
    for i in range(2):
        WebDriverWait(driver, 4).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    feedback_logger.debug("팝업 확인 작업 완료.")

def lab_manage_select_and_insert_user_number(lab, time, num=0, day=None, month=None, year=None):
    feedback_logger.debug(f"\"{lab}\" 실습실 {time}교시 입력 작업 시작.")
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)
    lab_manage_select_time(time)
    lab_manage_insert_user_number(num)
    feedback_logger.debug(f"\"{lab}\" 실습실 {time}교시 입력 작업 완료.")

def lab_manage_select_and_insert_lecture_schedule(lab, time, day=None, month=None, year=None):
    feedback_logger.debug("강의 일정 입력 작업 시작.")
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)
    lab_manage_select_time(time)
    lab_manage_insert_lecture_schedule()
    feedback_logger.debug("강의 일정 입력 작업 완료.")

def lab_manage_delete_record():
    feedback_logger.debug("기록 삭제 작업 시작.")
    delete_button = driver.find_element(By.NAME, "btnDelete")
    delete_button.click()
    send_popup_OK_twice()
    feedback_logger.debug("기록 삭제 작업 완료.")

def lab_manage_select_and_delete_record(lab, time, day=None, month=None, year=None):
    feedback_logger.debug("기록 선택 및 삭제 작업 시작.")
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)
    lab_manage_select_time(time)
    lab_manage_delete_record()
    feedback_logger.debug("기록 선택 및 삭제 작업 완료.")

def lab_manage_read_use_table():
    feedback_logger.debug("사용 테이블 읽기 작업 시작.")
    use_table = {}
    rows = driver.find_elements(By.CSS_SELECTOR, "#gvList tbody tr")

    for row in rows:
        date_cell = row.find_element(By.CSS_SELECTOR, "td")
        text_in_row = date_cell.text
        if text_in_row == "조회된 Data가 존재 하지 않습니다":
            break

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)")
        time_in_row = int(date_cell.text)

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
        user_number = int(date_cell.text.strip()) if date_cell.text.strip() else -1

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)")
        use_type = date_cell.text.strip()

        use_table[time_in_row] = {'type': use_type, 'number': user_number}

    feedback_logger.debug("사용 테이블 읽기 작업 완료.")
    return use_table

def lab_manage_read_user_number_at_time(time):
    feedback_logger.debug(f"{time}시 사용자 수 읽기 작업 시작.")
    use_table = lab_manage_read_use_table()
    user_number = use_table[time]['number']
    feedback_logger.debug(f"{time}시 사용자 수: {user_number}")
    return user_number

def lab_manage_read_use_type_at_time(time):
    feedback_logger.debug(f"{time}시 사용 유형 읽기 작업 시작.")
    use_table = lab_manage_read_use_table()
    use_type = use_table[time]['type']
    feedback_logger.debug(f"{time}시 사용 유형: {use_type}")
    return use_type

def lab_manage_is_record_exist_at_time(time):
    feedback_logger.debug(f"{time}시 기록 존재 여부 확인 작업 시작.")
    use_table = lab_manage_read_use_table()
    exists = use_table.get(time) is not None
    feedback_logger.debug(f"{time}시 기록 존재 여부: {exists}")
    return exists
