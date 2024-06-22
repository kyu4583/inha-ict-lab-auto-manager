import datetime
import logging

import enums
import page_driver as pd

feedback_logger = logging.getLogger('feedback_logger')
console_logger = logging.getLogger('console_logger')

def manage_lab_today(lab):
    today_date = datetime.date.today()
    manage_lab_at_date(today_date, lab)


def manage_lab_at_date(target_date, lab):
    feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 입력 시작..")
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
        feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 입력 시작..")
        if enums.Schedule[lab.name].value[day_of_target][i - 1] == 0:
            if use_table.get(i) is None:
                pd.lab_manage_select_and_insert_user_number(lab, i, 0, day, month, year)
        elif enums.Schedule[lab.name].value[day_of_target][i - 1] == 1:
            if use_table.get(i) is None:
                pd.lab_manage_select_and_insert_lecture_schedule(lab, i, day, month, year)
        feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 입력 완료.")

    feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 입력 완료.")

def manage_lab_at_range_of_date(lab, start_date, end_date, except_dates):
    feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 입력 시작..(예외: {except_dates})")
    if start_date > end_date:
        while start_date >= end_date:
            if start_date not in except_dates:
                manage_lab_at_date(start_date, lab)
            start_date = start_date - datetime.timedelta(days=1)
    else:
        while start_date <= end_date:
            if start_date not in except_dates:
                manage_lab_at_date(start_date, lab)
            start_date = start_date + datetime.timedelta(days=1)
    feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 입력 완료.(예외: {except_dates})")


def delete_lab_at_date(target_date, lab):
    feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 삭제 시작..")
    day = target_date.day
    month = target_date.month
    year = target_date.year

    day_of_target = target_date.strftime('%A')
    if enums.Schedule[lab.name].value.get(day_of_target) is None:
        feedback_logger.info("기록이 이미 비어있습니다.")
        return 0

    pd.lab_manage_select_date(day, month, year)
    pd.lab_manage_select_lab(lab)
    for i in range(1, 25):
        if pd.lab_manage_is_record_exist_at_time(i):
            pd.lab_manage_select_time(i)
            feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 삭제 시작..")
            pd.lab_manage_delete_record()
            feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] {i}교시 삭제 완료.")

    feedback_logger.info(f"[대상 날짜: {target_date}], [실습실: {lab.name}] 삭제 완료.")

def delete_lab_records_at_range_of_date(lab, start_date, end_date, except_dates):
    feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 삭제 시작..(예외: {except_dates})")
    if start_date > end_date:
        while start_date >= end_date:
            if start_date not in except_dates:
                delete_lab_at_date(start_date, lab)
            start_date = start_date - datetime.timedelta(days=1)
    else:
        while start_date <= end_date:
            if start_date not in except_dates:
                delete_lab_at_date(start_date, lab)
            start_date = start_date + datetime.timedelta(days=1)
    feedback_logger.info(f"[대상 날짜: {start_date}~{end_date}], [실습실: {lab.name}] 삭제 완료.(예외: {except_dates})")