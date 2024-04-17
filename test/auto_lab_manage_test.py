import datetime
import unittest

import auto_lab_manager as lm
import enums
import page_driver as pd


class TestMyFunction(unittest.TestCase):
    def test_오늘_모든실습실_자동입력_테스트(self):
        today = datetime.datetime.now().strftime('%A')
        for lab in enums.Lab:
            schedule = enums.get(enums.Schedule, lab.name)
            if schedule is not None and schedule.value.get(today) is not None:
                pd.open_portal()
                pd.log_in()
                pd.open_ins_from_portal_after_login()
                pd.open_lab_manage_from_ins()
                pd.lab_manage_select_lab(lab)
                origin_use_table = pd.lab_manage_read_use_table()
                pd.reset_driver()

                #테스트 대상 메소드
                lm.manage_lab_today(lab)

                editted_use_table = pd.lab_manage_read_use_table()

                for time in origin_use_table:
                    editted_use_table.pop(time)

                for time in editted_use_table:
                    if enums.get(enums.Schedule, lab.name).value.get(today)[time - 1] == 1:
                        self.assertEqual(editted_use_table[time]['type'], '수업')
                    else:
                        self.assertEqual(editted_use_table[time]['type'], '')

                for time in editted_use_table:
                    pd.lab_manage_select_time(time)
                    pd.lab_manage_delete_record()

                final_use_table = pd.lab_manage_read_use_table()
                self.assertEqual(origin_use_table, final_use_table)

                pd.reset_driver()