import datetime
import pytest

import auto_lab_manager as lm
import enums
import page_driver as pd


def test_오늘_모든실습실_자동입력_테스트():
    pd.start_and_enter_lab_manage_handling_except()
    today = datetime.datetime.now().strftime('%A')
    for lab in enums.Lab:
        schedule = enums.get(enums.Schedule, lab.name)
        if schedule is not None and schedule.value.get(today) is not None:
            pd.lab_manage_select_lab(lab)
            origin_use_table = pd.lab_manage_read_use_table()

            # 테스트 대상 메소드
            lm.manage_lab_today(lab)

            editted_use_table = pd.lab_manage_read_use_table()

            for time in origin_use_table:
                editted_use_table.pop(time)

            for time in editted_use_table:
                if enums.get(enums.Schedule, lab.name).value.get(today)[time - 1] == 1:
                    assert editted_use_table[time]['type'] == '수업'
                else:
                    assert editted_use_table[time]['type'].strip() == ''

            for time in editted_use_table:
                pd.lab_manage_select_time(time)
                pd.lab_manage_delete_record()

            final_use_table = pd.lab_manage_read_use_table()
            assert origin_use_table == final_use_table

def test_하루기록_전체삭제_테스트():
    for i in range(1, 25):
        pd.lab_manage_select_and_insert_lecture_schedule(enums.Lab.L60_808, i, 30, 12, 2000)

    lm.delete_lab_at_date(datetime.date(2000, 12, 30), enums.Lab.L60_808)

    for i in range(1, 25):
        assert not pd.lab_manage_is_record_exist_at_time(i)