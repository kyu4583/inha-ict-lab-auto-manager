import logging
import time
import uuid

from selenium.common import UnexpectedAlertPresentException, TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import calendar_manager as cm
import config
import datetime

import enums

feedback_logger = logging.getLogger('feedback_logger')
console_logger = logging.getLogger('console_logger')

class PageDriver:
    def __init__(self):
        self.id = uuid.uuid4()
        self.web_driver = config.create_web_driver()

    def __del__(self):
        config.quit_web_driver(self.web_driver)

    def reset_web_driver(self):
        config.quit_web_driver(self.web_driver)
        self.web_driver = config.create_web_driver()

    def quit_web_driver(self):
        config.quit_web_driver(self.web_driver)

    def get_web_driver(self):
        return self.web_driver

    def open_url(self, url):
        time.sleep(0.01)
        self.web_driver.get(url)

    def open_portal(self):
        feedback_logger.info("포털 접속중..")
        self.open_url("https://portal.inha.ac.kr")
        feedback_logger.info("포털 접속 완료.")

    def log_in(self, id = None, pw = None):
        if id is None:
            id = config.get_default_portal_id()
        if pw is None:
            pw = config.get_default_portal_pw()

        feedback_logger.info("로그인 시도 중...")

        user_id_input = WebDriverWait(self.web_driver, 4).until(
            EC.presence_of_element_located((By.ID, "userId"))
        )
        password_input = WebDriverWait(self.web_driver, 4).until(
            EC.presence_of_element_located((By.ID, "passwd"))
        )
        user_id_input.send_keys(id)
        password_input.send_keys(pw)
        login_button = WebDriverWait(self.web_driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='ep-btnid']"))
        )
        login_button.click()
        feedback_logger.info("로그인 완료.")

    def log_out(self):
        feedback_logger.info("로그아웃 시도 중...")
        try:
            self.open_portal()
            logout_button = WebDriverWait(self.web_driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id=\"gnb\"]/ul/li[5]/a"))
            )
            logout_button.click()
        except UnexpectedAlertPresentException as e:
            alert = Alert(self.web_driver)
            alert_text = alert.text
            if "사용자 세션이 만료 되었습니다. 자동 로그아웃 처리 됩니다." in alert_text:
                pass
            else:
                raise e

        feedback_logger.info("로그아웃 완료.")

    def logout_and_reset_web_driver(self):
        try:
            self.log_out()
        except Exception as e:
            pass
        self.reset_web_driver()

    def open_ins_from_portal_after_login(self):
        feedback_logger.info("학사행정 페이지로 이동 중...")
        self.open_url("https://ins2.inha.ac.kr/ins/")
        feedback_logger.info("학사행정 페이지 접속 완료.")

    def start_and_enter_lab_manage(self, id=None, pw=None):
        self.open_portal()
        if id is None:
            self.log_in()
        else:
            self.log_in(id, pw)
        self.open_ins_from_portal_after_login()
        self.open_lab_manage_from_ins()

    def handle_alert_or_timeout_and_retry(self, action, max_retries=15):
        retries = 0
        while retries < max_retries:
            try:
                self.logout_and_reset_web_driver()
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

    def start_and_enter_lab_manage_handling_except(self, id=None, pw=None):
        self.handle_alert_or_timeout_and_retry(lambda: self.start_and_enter_lab_manage(id, pw))

    def frame_insMain(self):
        self.switch_default_content()
        WebDriverWait(self.web_driver, 4).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "INSMain"))
        )

    def frame_insMain_main(self):
        self.switch_default_content()
        self.frame_insMain()
        WebDriverWait(self.web_driver, 4).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "Main"))
        )

    def frame_insMain_left(self):
        self.switch_default_content()
        self.frame_insMain()
        WebDriverWait(self.web_driver, 4).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "Left"))
        )

    def frame_insMain_main_ifTab(self):
        self.switch_default_content()
        self.frame_insMain_main()
        WebDriverWait(self.web_driver, 4).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ifTab"))
        )

    def open_lab_manage_from_ins(self):
        feedback_logger.debug("실습실 관리 탭 이동 중...")
        self.switch_default_content()
        self.frame_insMain()
        self.frame_insMain_main()
        self.frame_insMain_left()

        # '정보통신' 메뉴 클릭을 위한 XPath 사용
        info_comm_link = self.web_driver.find_element(By.ID, 'JB_03006')
        info_comm_link.click()

        button = WebDriverWait(self.web_driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="SideMenu"]/ul/li[12]/ul/li/a'))
        )
        button.click()
        feedback_logger.debug("실습실 관리 탭 이동 완료.")

    def switch_default_content(self):
        # 메인 컨텐츠로 컨텍스트 전환
        self.web_driver.switch_to.default_content()

    def lab_manage_select_date(self, day=None, month=None, year=None):
        feedback_logger.debug("날짜 선택 중...")
        today = datetime.date.today()
        if year is None:
            year = today.year
        if month is None:
            month = today.month
        if day is None:
            day = today.day

        self.frame_insMain_main_ifTab()

        button = WebDriverWait(self.web_driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/form/table/tbody/tr[1]/td[1]/img'))
        )
        button.click()

        cm.add_monthly_calendar(month, year)
        coordinates = cm.calendar_data[year][month]['coordinates']

        year_select_element = WebDriverWait(self.web_driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div[1]/div/select[1]')
            )
        )
        year_select = Select(year_select_element)
        year_select.select_by_value(str(year))

        month_select_element = WebDriverWait(self.web_driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div/div[1]/div/select[2]')
            )
        )
        month_select = Select(month_select_element)
        month_select.select_by_value(str(month - 1))

        day_button = WebDriverWait(self.web_driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'/html/body/div/table/tbody/tr[{coordinates[day][0]}]/td[{coordinates[day][1]}]/a'))
        )
        day_button.click()
        feedback_logger.debug("날짜 선택 완료.")

    def lab_manage_select_lab(self, lab):
        feedback_logger.debug("실습실 선택 중...")
        self.frame_insMain_main_ifTab()

        # 실습실 선택
        lab_select_element = WebDriverWait(self.web_driver, 4).until(
            EC.presence_of_element_located((By.ID, "ddlLabList"))
        )
        lab_select = Select(lab_select_element)
        lab_select.select_by_value(lab.value)
        feedback_logger.debug("실습실 선택 완료.")

    def lab_manage_search(self):
        self.frame_insMain_main_ifTab()

        # 조회 버튼 클릭
        search_button = self.web_driver.find_element(By.ID, "btnSearch")
        search_button.click()

    def lab_manage_select_time(self, time):
        feedback_logger.debug(f"{time}교시 선택 중...")
        self.frame_insMain_main_ifTab()

        # 시간 선택
        time_select_element = WebDriverWait(self.web_driver, 4).until(
            EC.presence_of_element_located((By.ID, "ddlTimeList"))
        )
        time_select = Select(time_select_element)
        time_select.select_by_value(str(time))
        feedback_logger.debug(f"{time}교시 선택 완료.")

    def lab_manage_insert_user_number(self, num=0):
        feedback_logger.debug(f"사용자 수 {num} 입력 중...")
        user_number_input = self.web_driver.find_element(By.ID, "txtInwon")

        user_number_input.send_keys(num)

        user_number_select_element = WebDriverWait(self.web_driver, 4).until(
            EC.presence_of_element_located((By.ID, "ddlUseGubun"))
        )
        user_number_select = Select(user_number_select_element)
        user_number_select.select_by_value("0")

        # 저장 버튼 클릭
        save_button = self.web_driver.find_element(By.NAME, "btnSave")
        save_button.click()

        # 팝업 확인 * 2번
        self.send_popup_OK_twice()
        feedback_logger.debug(f"사용자 수 {num} 입력 완료.")

    def lab_manage_insert_lecture_schedule(self):
        feedback_logger.debug("강의 일정 입력 시작.")
        user_number_select_element = WebDriverWait(self.web_driver, 4).until(
            EC.presence_of_element_located((By.ID, "ddlUseGubun"))
        )
        user_number_select = Select(user_number_select_element)
        user_number_select.select_by_value("01")

        save_button = self.web_driver.find_element(By.NAME, "btnSave")
        save_button.click()

        self.send_popup_OK_twice()
        feedback_logger.debug("강의 일정 입력 완료.")

    def send_popup_OK_twice(self):
        feedback_logger.debug("팝업 확인 작업 시작.")
        for i in range(2):
            WebDriverWait(self.web_driver, 4).until(EC.alert_is_present())
            alert = self.web_driver.switch_to.alert
            alert.accept()
        feedback_logger.debug("팝업 확인 작업 완료.")

    def lab_manage_select_and_insert_user_number(self, lab, time, num=0, day=None, month=None, year=None):
        feedback_logger.debug(f"\"{lab}\" 실습실 {time}교시 입력 작업 시작.")
        self.lab_manage_select_date(day, month, year)
        self.lab_manage_select_lab(lab)
        self.lab_manage_select_time(time)
        self.lab_manage_insert_user_number(num)
        feedback_logger.debug(f"\"{lab}\" 실습실 {time}교시 입력 작업 완료.")

    def lab_manage_select_and_insert_lecture_schedule(self, lab, time, day=None, month=None, year=None):
        feedback_logger.debug("강의 일정 입력 작업 시작.")
        self.lab_manage_select_date(day, month, year)
        self.lab_manage_select_lab(lab)
        self.lab_manage_select_time(time)
        self.lab_manage_insert_lecture_schedule()
        feedback_logger.debug("강의 일정 입력 작업 완료.")

    def lab_manage_delete_record(self):
        feedback_logger.debug("기록 삭제 작업 시작.")
        delete_button = self.web_driver.find_element(By.NAME, "btnDelete")
        delete_button.click()
        self.send_popup_OK_twice()
        feedback_logger.debug("기록 삭제 작업 완료.")

    def lab_manage_select_and_delete_record(self, lab, time, day=None, month=None, year=None):
        feedback_logger.debug("기록 선택 및 삭제 작업 시작.")
        self.lab_manage_select_date(day, month, year)
        self.lab_manage_select_lab(lab)
        self.lab_manage_select_time(time)
        self.lab_manage_delete_record()
        feedback_logger.debug("기록 선택 및 삭제 작업 완료.")

    def lab_manage_read_use_table(self):
        feedback_logger.debug("사용 테이블 읽기 작업 시작.")
        use_table = {}
        rows = self.web_driver.find_elements(By.CSS_SELECTOR, "#gvList tbody tr")

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

    def lab_manage_read_user_number_at_time(self, time):
        feedback_logger.debug(f"{time}시 사용자 수 읽기 작업 시작.")
        use_table = self.lab_manage_read_use_table()
        user_number = use_table[time]['number']
        feedback_logger.debug(f"{time}시 사용자 수: {user_number}")
        return user_number

    def lab_manage_read_use_type_at_time(self, time):
        feedback_logger.debug(f"{time}시 사용 유형 읽기 작업 시작.")
        use_table = self.lab_manage_read_use_table()
        use_type = use_table[time]['type']
        feedback_logger.debug(f"{time}시 사용 유형: {use_type}")
        return use_type

    def lab_manage_is_record_exist_at_time(self, time):
        feedback_logger.debug(f"{time}시 기록 존재 여부 확인 작업 시작.")
        use_table = self.lab_manage_read_use_table()
        exists = use_table.get(time) is not None
        feedback_logger.debug(f"{time}시 기록 존재 여부: {exists}")
        return exists

    def manage_lab_today(self, lab):
        today_date = datetime.date.today()
        self.manage_lab_at_date(today_date, lab)

    def manage_lab_at_date(self, target_date, lab):
        feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 입력 시작..")
        day = target_date.day
        month = target_date.month
        year = target_date.year

        day_of_target = target_date.strftime('%A')
        if enums.Schedule[lab.name].value.get(day_of_target) is None:
            return 0

        self.lab_manage_select_date(day, month, year)
        self.lab_manage_select_lab(lab)

        use_table = self.lab_manage_read_use_table()

        for i in range(1, 25):
            feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 입력 시작..")
            if enums.Schedule[lab.name].value[day_of_target][i - 1] == 0:
                if use_table.get(i) is None:
                    self.lab_manage_select_and_insert_user_number(lab, i, 0, day, month, year)
            elif enums.Schedule[lab.name].value[day_of_target][i - 1] == 1:
                if use_table.get(i) is None:
                    self.lab_manage_select_and_insert_lecture_schedule(lab, i, day, month, year)
            feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 입력 완료.")

        feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 입력 완료.")

    def manage_lab_at_range_of_date(self, lab, start_date, end_date, except_dates):
        feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 입력 시작..(예외: {except_dates})")
        if start_date > end_date:
            while start_date >= end_date:
                if start_date not in except_dates:
                    self.manage_lab_at_date(start_date, lab)
                start_date = start_date - datetime.timedelta(days=1)
        else:
            while start_date <= end_date:
                if start_date not in except_dates:
                    self.manage_lab_at_date(start_date, lab)
                start_date = start_date + datetime.timedelta(days=1)
        feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 입력 완료.(예외: {except_dates})")

    def delete_lab_at_date(self, target_date, lab):
        feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 삭제 시작..")
        day = target_date.day
        month = target_date.month
        year = target_date.year

        self.lab_manage_select_date(day, month, year)
        self.lab_manage_select_lab(lab)
        for i in range(1, 25):
            if self.lab_manage_is_record_exist_at_time(i):
                self.lab_manage_select_time(i)
                feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 삭제 시작..")
                self.lab_manage_delete_record()
                feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 삭제 완료.")

        feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 삭제 완료.")

    def delete_lab_records_at_range_of_date(self, lab, start_date, end_date, except_dates):
        feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 삭제 시작..(예외: {except_dates})")
        if start_date > end_date:
            while start_date >= end_date:
                if start_date not in except_dates:
                    self.delete_lab_at_date(start_date, lab)
                start_date = start_date - datetime.timedelta(days=1)
        else:
            while start_date <= end_date:
                if start_date not in except_dates:
                    self.delete_lab_at_date(start_date, lab)
                start_date = start_date + datetime.timedelta(days=1)
        feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 삭제 완료.(예외: {except_dates})")
