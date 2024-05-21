import os
import time

from selenium.common import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import calendar_manager as cm
import config
import datetime

driver = config.Driver.get_instance()


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
    open_url("https://portal.inha.ac.kr")


def log_in(id=os.getenv("INHA_PORTAL_ID"), pw=os.getenv("INHA_PORTAL_PW")):
    # WebDriverWait를 사용해 요소가 로드될 때까지 대기
    user_id_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "userId"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passwd"))
    )

    # 아이디, 비번 입력
    user_id_input.send_keys(id)
    password_input.send_keys(pw)

    # 로그인 버튼 클릭
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@class='ep-btnid']"))
    )
    login_button.click()


def log_out():
    open_portal()

    # 로그아웃 버튼 클릭
    logout_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id=\"gnb\"]/ul/li[5]/a"))
    )
    logout_button.click()


def open_ins_from_portal_after_login():
    open_url("https://ins2.inha.ac.kr/ins/")


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
        except (UnexpectedAlertPresentException):
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            retries += 1
        except (TimeoutException):
            retries += 1
        except Exception as e:
            retries += 1
    raise Exception("Max retries exceeded")


def start_and_enter_lab_manage_handling_except(id=None, pw=None):
    handle_alert_or_timeout_and_retry(lambda: start_and_enter_lab_manage(id, pw))



def frame_insMain():
    switch_default_content()
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "INSMain"))
    )


def frame_insMain_main():
    switch_default_content()
    frame_insMain()
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "Main"))
    )


def frame_insMain_left():
    switch_default_content()
    frame_insMain()
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "Left"))
    )


def frame_insMain_main_ifTab():
    switch_default_content()
    frame_insMain_main()
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "ifTab"))
    )


def open_lab_manage_from_ins():
    switch_default_content()
    frame_insMain()
    frame_insMain_main()
    frame_insMain_left()

    # '정보통신' 메뉴 클릭을 위한 XPath 사용
    info_comm_link = driver.find_element(By.ID, 'JB_03006')
    info_comm_link.click()

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="SideMenu"]/ul/li[11]/ul/li/a'))
    )
    button.click()


def switch_default_content():
    # 메인 컨텐츠로 컨텍스트 전환
    driver.switch_to.default_content()


def lab_manage_select_date(day=None, month=None, year=None):
    today = datetime.date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    if day is None:
        day = today.day

    frame_insMain_main_ifTab()

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/form/table/tbody/tr[1]/td[1]/img'))
    )
    button.click()

    cm.add_monthly_calendar(month, year)
    coordinates = cm.calendar_data[year][month]['coordinates']

    year_select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[1]/div/select[1]')
        )
    )
    year_select = Select(year_select_element)
    year_select.select_by_value(str(year))

    month_select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[1]/div/select[2]')
        )
    )
    month_select = Select(month_select_element)
    month_select.select_by_value(str(month - 1))

    day_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, f'/html/body/div/table/tbody/tr[{coordinates[day][0]}]/td[{coordinates[day][1]}]/a'))
    )
    day_button.click()


def lab_manage_select_lab(lab):
    frame_insMain_main_ifTab()

    # 실습실 선택
    lab_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ddlLabList"))
    )
    lab_select = Select(lab_select_element)
    lab_select.select_by_value(lab.value)


def lab_manage_search():
    frame_insMain_main_ifTab()

    # 조회 버튼 클릭
    search_button = driver.find_element(By.ID, "btnSearch")
    search_button.click()


def lab_manage_select_time(time):
    frame_insMain_main_ifTab()

    # 실습실 선택
    time_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ddlTimeList"))
    )
    time_select = Select(time_select_element)
    time_select.select_by_value(str(time))


def lab_manage_insert_user_number(num=0):
    user_number_input = driver.find_element(By.ID, "txtInwon")

    user_number_input.send_keys(num)

    user_number_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ddlUseGubun"))
    )
    user_number_select = Select(user_number_select_element)
    user_number_select.select_by_value("0")

    # 저장 버튼 클릭
    save_button = driver.find_element(By.NAME, "btnSave")
    save_button.click()

    # 팝업 확인 * 2번
    send_popup_OK_twice()


def lab_manage_insert_lecture_schedule():
    user_number_select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ddlUseGubun"))
    )
    user_number_select = Select(user_number_select_element)
    user_number_select.select_by_value("01")

    # 저장 버튼 클릭
    save_button = driver.find_element(By.NAME, "btnSave")
    save_button.click()

    # 팝업 확인 * 2번
    send_popup_OK_twice()


def send_popup_OK_twice():
    for i in range(2):
        # 팝업 대기 및 접근
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        # 팝업에 있는 'OK' 버튼 클릭
        alert = driver.switch_to.alert
        alert.accept()


def lab_manage_select_and_insert_user_number(lab, time, num=0, day=None, month=None, year=None):
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)
    lab_manage_select_time(time)
    lab_manage_insert_user_number(num)


def lab_manage_select_and_insert_lecture_schedule(lab, time, day=None, month=None, year=None):
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)
    lab_manage_select_time(time)
    lab_manage_insert_lecture_schedule()


def lab_manage_delete_record():
    # 삭제 버튼 클릭
    delete_button = driver.find_element(By.NAME, "btnDelete")
    delete_button.click()

    # 팝업 확인 * 2번
    send_popup_OK_twice()


def lab_manage_select_and_delete_record(lab, time, day=None, month=None, year=None):
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)
    lab_manage_select_time(time)

    lab_manage_delete_record()


def lab_manage_select_day_and_delete_all(lab, day=None, month=None, year=None):
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)

    for i in range(1, 25):
        if lab_manage_is_record_exist_at_time(i):
            lab_manage_select_time(i)
            lab_manage_delete_record()


def lab_manage_read_use_table():
    use_table = {}

    # 테이블의 모든 행을 찾음
    rows = driver.find_elements(By.CSS_SELECTOR, "#gvList tbody tr")

    # 각 행에 대해 반복
    for row in rows:
        date_cell = row.find_element(By.CSS_SELECTOR, "td")
        text_in_row = date_cell.text
        if text_in_row == "조회된 Data가 존재 하지 않습니다":
            break

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)")
        time_in_row = int(date_cell.text)

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
        if date_cell.text == ' ':
            user_number = -1
        else:
            user_number = int(date_cell.text.strip())

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)")
        use_type = date_cell.text.strip()

        use_table[time_in_row] = {'type': use_type, 'number': user_number}

    return use_table


def lab_manage_read_user_number_at_time(time):
    use_table = lab_manage_read_use_table()
    return use_table[time]['number']


def lab_manage_read_use_type_at_time(time):
    use_table = lab_manage_read_use_table()
    return use_table[time]['type']


def lab_manage_is_record_exist_at_time(time):
    use_table = lab_manage_read_use_table()
    return use_table.get(time) is not None
