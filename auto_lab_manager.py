import datetime

import enums
import page_driver as pd


def manage_lab_today(lab):
    today_date = datetime.date.today()
    manage_lab_at_date(today_date, lab)


def manage_lab_at_date(target_date, lab):
    day = target_date.day
    month = target_date.month
    year = target_date.year

    day_of_target = target_date.strftime('%A')

    pd.open_portal()
    pd.log_in()
    pd.open_ins_from_portal_after_login()
    pd.open_lab_manage_from_ins()
    pd.lab_manage_select_lab(lab)

    use_table = pd.lab_manage_read_use_table()

    for i in range(1, 25):
        if enums.Schedule[lab.name].value[day_of_target][i - 1] == 0:
            if use_table.get(i) is None:
                pd.lab_manage_select_and_insert_user_number(lab, i, 0, day, month, year)
        elif enums.Schedule[lab.name].value[day_of_target][i - 1] == 1:
            if use_table.get(i) is None:
                pd.lab_manage_select_and_insert_lecture_schedule(lab, i, day, month, year)
