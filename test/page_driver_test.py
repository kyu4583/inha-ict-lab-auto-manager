import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import enums
import page_driver as pd


@pytest.fixture(scope="module", autouse=True)
def initial_setup_teardown():
    pd.reset_driver()
    pd.start_and_enter_lab_manage_handling_except()
    yield
    pd.logout_and_reset_driver()

@pytest.fixture(autouse=True)
def setup_teardown_each():
    yield
    pd.logout_and_reset_driver()
    pd.start_and_enter_lab_manage_handling_except()

def test_현재_조회일자_선택_테스트():
    pd.lab_manage_select_date(24, 4, 2024)
    pd.lab_manage_select_lab(enums.Lab.L60_808)
    pd.lab_manage_search()

    element = pd.WebDriverWait(pd.get_driver(), 4).until(
        pd.EC.presence_of_element_located((pd.By.ID, "txtUseDate"))
    )
    date_value = element.get_attribute('value')
    assert date_value == "2024-04-24"


def test_과거_조회일자_선택_테스트():
    pd.lab_manage_select_date(24, 3, 2022)
    pd.lab_manage_select_lab(enums.Lab.L60_808)
    pd.lab_manage_search()

    element = pd.WebDriverWait(pd.get_driver(), 4).until(
        pd.EC.presence_of_element_located((pd.By.ID, "txtUseDate"))
    )
    date_value = element.get_attribute('value')
    assert date_value == "2022-03-24"


def test_실습실_선택_테스트():
    def get_selected_lab_text():
        pd.frame_insMain_main_ifTab()

        lab_select_element = WebDriverWait(pd.get_driver(), 4).until(
            EC.presence_of_element_located((By.ID, "ddlLabList"))
        )
        lab_select = Select(lab_select_element)

        # 선택된 옵션을 얻음
        selected_option = lab_select.first_selected_option

        return selected_option.get_attribute('value')
    for lab in enums.Lab:
        pd.lab_manage_select_lab(lab)
        assert lab.value == get_selected_lab_text()


def test_이용현황_입력_및_기록조회_테스트():
    pd.lab_manage_select_and_insert_user_number(enums.Lab.L5E_116, 12, 5, 30, 12, 2000)

    assert pd.lab_manage_read_use_type_at_time(12).strip() == ''
    assert pd.lab_manage_read_user_number_at_time(12) == 5

    pd.lab_manage_select_and_delete_record(enums.Lab.L5E_116, 12, 30, 12, 2000)


def test_수업일정_입력_및_기록조회_테스트():
    pd.lab_manage_select_and_insert_lecture_schedule(enums.Lab.L5E_116, 13, 30, 12, 2000)

    assert pd.lab_manage_read_use_type_at_time(13).strip() == '수업'

    pd.lab_manage_select_and_delete_record(enums.Lab.L5E_116, 13, 30, 12, 2000)
