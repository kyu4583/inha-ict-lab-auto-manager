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

    def test_조회일자_선택_테스트(self):
        pd.open_portal()
        pd.log_in(os.getenv("PORTAL_ID"), os.getenv("PORTAL_PW"))
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

    def test_실습실_선택_테스트(self):
        pd.open_portal()
        pd.log_in(os.getenv("PORTAL_ID"), os.getenv("PORTAL_PW"))
        pd.open_ins_from_portal_after_login()
        pd.open_lab_manage_from_ins()

        # 모든 실습실에 대해 선택 테스트
        for lab in enums.Lab:
            pd.lab_manage_select_lab(lab)
            self.assertEqual(lab.value, get_selected_lab_text())
