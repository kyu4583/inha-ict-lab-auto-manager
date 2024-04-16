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
    month_select.select_by_value(str(month-1))

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
