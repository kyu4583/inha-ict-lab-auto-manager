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
    if enums.Schedule[lab.name].value.get(day_of_target) is None:
        return 0

    pd.lab_manage_select_date(day, month, year)
    pd.lab_manage_select_lab(lab)

    use_table = pd.lab_manage_read_use_table()

    for i in range(1, 25):
        if enums.Schedule[lab.name].value[day_of_target][i - 1] == 0:
            if use_table.get(i) is None:
                pd.lab_manage_select_and_insert_user_number(lab, i, 0, day, month, year)
        elif enums.Schedule[lab.name].value[day_of_target][i - 1] == 1:
            if use_table.get(i) is None:
                pd.lab_manage_select_and_insert_lecture_schedule(lab, i, day, month, year)


def manage_lab_at_range_of_date(lab, start_date, end_date, except_date):
    if start_date > end_date:
        while start_date >= end_date:
            if start_date not in except_date:
                manage_lab_at_date(start_date, lab)
            start_date = start_date - datetime.timedelta(days=1)
    else:
        while start_date <= end_date:
            if start_date not in except_date:
                manage_lab_at_date(start_date, lab)
            start_date = start_date + datetime.timedelta(days=1)