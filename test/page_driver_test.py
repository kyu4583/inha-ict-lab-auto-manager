import os
import unittest
import config
import page_driver as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestMyFunction(unittest.TestCase):
    def test_조회일자_선택_테스트(self):
        driver = config.Driver.get_instance()
        pd.open_portal()
        pd.log_in(os.getenv("PORTAL_ID"), os.getenv("PORTAL_PW"))
        pd.open_ins_from_portal_after_login()
        pd.lab_manage_select_date(24, 4, 2024)

        # 실습실 선택
        lab_select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ddlLabList"))
        )
        lab_select = Select(lab_select_element)
        lab_select.select_by_value("60주년-808")

        # 조회 버튼 클릭
        search_button = driver.find_element(By.ID, "btnSearch")
        search_button.click()

        # 입력 필드의 값을 검색
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtUseDate"))
        )
        date_value = element.get_attribute('value')

        # 조회일자가 "2024-04-24"로 선택되어 있는지 확인
        self.assertEqual("2024-04-24", date_value)