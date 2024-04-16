import os
import unittest

from selenium.webdriver.support.select import Select

import config
import enums
import page_driver as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_selected_lab_text():
    pd.frame_insMain_main_ifTab()

    lab_select_element = WebDriverWait(pd.get_driver(), 10).until(
        EC.presence_of_element_located((By.ID, "ddlLabList"))
    )
    lab_select = Select(lab_select_element)

    # 선택된 옵션을 얻음
    selected_option = lab_select.first_selected_option

    return selected_option.get_attribute('value')


class TestMyFunction(unittest.TestCase):

    def tearDown(self):
        pd.reset_driver()

    def test_현재_조회일자_선택_테스트(self):
        pd.open_portal()
        pd.log_in(os.getenv("INHA_PORTAL_ID"), os.getenv("INHA_PORTAL_PW"))
        pd.open_ins_from_portal_after_login()
        pd.open_lab_manage_from_ins()
        pd.lab_manage_select_date(24, 4, 2024)
        pd.lab_manage_select_lab(enums.Lab.L60_808)
        pd.lab_manage_search()

        # 입력 필드의 값을 검색
        element = WebDriverWait(pd.get_driver(), 10).until(
            EC.presence_of_element_located((By.ID, "txtUseDate"))
        )
        date_value = element.get_attribute('value')

        # 조회일자가 "2024-04-24"로 선택되어 있는지 확인
        self.assertEqual("2024-04-24", date_value)

    def test_과거_조회일자_선택_테스트(self):
        pd.open_portal()
        pd.log_in(os.getenv("INHA_PORTAL_ID"), os.getenv("INHA_PORTAL_PW"))
        pd.open_ins_from_portal_after_login()
        pd.open_lab_manage_from_ins()
        pd.lab_manage_select_date(24, 3, 2022)
        pd.lab_manage_select_lab(enums.Lab.L60_808)
        pd.lab_manage_search()

        # 입력 필드의 값을 검색
        element = WebDriverWait(pd.get_driver(), 10).until(
            EC.presence_of_element_located((By.ID, "txtUseDate"))
        )
        date_value = element.get_attribute('value')

        # 조회일자가 "2022-03-24"로 선택되어 있는지 확인
        self.assertEqual("2022-03-24", date_value)

    def test_실습실_선택_테스트(self):
        pd.open_portal()
        pd.log_in(os.getenv("INHA_PORTAL_ID"), os.getenv("INHA_PORTAL_PW"))
        pd.open_ins_from_portal_after_login()
        pd.open_lab_manage_from_ins()

        # 모든 실습실에 대해 선택 테스트
        for lab in enums.Lab:
            pd.lab_manage_select_lab(lab)
            self.assertEqual(lab.value, get_selected_lab_text())

    def test_이용현황_입력_및_기록조회_테스트(self):
        pd.open_portal()
        pd.log_in(os.getenv("INHA_PORTAL_ID"), os.getenv("INHA_PORTAL_PW"))
        pd.open_ins_from_portal_after_login()
        pd.open_lab_manage_from_ins()

        # 더미 데이터 입력
        pd.lab_manage_select_and_insert_user_number(enums.Lab.L5E_116, 12, 5, 30, 12, 2000)

        # 조회 테스트
        self.assertEqual(pd.lab_manage_read_use_type_at_time(12).strip(), '')
        self.assertEqual(pd.lab_manage_read_user_number_at_time(12), 5)

        # 입력한 데이터 삭제
        pd.lab_manage_select_and_delete_record(enums.Lab.L5E_116, 12, 30, 12, 2000)