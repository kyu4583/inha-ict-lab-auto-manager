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


def open_url(url):
    driver.get(url)


def open_portal():
    open_url("https://portal.inha.ac.kr")


def log_in(id, pw):
    # 아이디와 비밀번호 입력 필드 찾기
    user_id_input = driver.find_element(By.ID, "userId")
    password_input = driver.find_element(By.ID, "passwd")
    # 아이디와 비밀번호 입력
    user_id_input.send_keys(id)
    password_input.send_keys(pw)
    # 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, "//input[@class='ep-btnid']")
    login_button.click()


def open_ins_from_portal_after_login():
    open_url("https://ins2.inha.ac.kr/ins/")


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


def lab_manage_select_and_delete_record(lab, time, day=None, month=None, year=None):
    lab_manage_select_date(day, month, year)
    lab_manage_select_lab(lab)
    lab_manage_select_time(time)

    # 삭제 버튼 클릭
    delete_button = driver.find_element(By.NAME, "btnDelete")
    delete_button.click()

    # 팝업 확인 * 2번
    send_popup_OK_twice()


def lab_manage_read_use_table():
    use_table = {}

    # 테이블의 모든 행을 찾음
    rows = driver.find_elements(By.CSS_SELECTOR, "#gvList tbody tr")

    # 각 행에 대해 반복
    for row in rows:
        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)")
        time_in_row = int(date_cell.text)

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)")
        if date_cell.text == ' ':
            user_number = -1
        else:
            user_number = int(date_cell.text)

        date_cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)")
        use_type = date_cell.text

        use_table[time_in_row] = {'type': use_type, 'number': user_number}

    return use_table


def lab_manage_read_user_number_at_time(time):
    use_table = lab_manage_read_use_table()
    return use_table[time]['number']

def lab_manage_read_use_type_at_time(time):
    use_table = lab_manage_read_use_table()
    return use_table[time]['type']