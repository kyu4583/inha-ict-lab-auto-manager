import datetime

import page_driver as pd
import auto_lab_manager as lm
import enums


def parse_date(date_str):
    today = datetime.datetime.today()
    try:
        # 'yy.mm.dd' 형식
        if len(date_str.split('.')) == 3:
            return datetime.datetime.strptime(date_str, "%y.%m.%d").date()
        # 'mm.dd' 형식
        elif len(date_str.split('.')) == 2:
            return datetime.datetime.strptime(f"{today.year}.{date_str}", "%Y.%m.%d").date()
        # 'dd' 형식
        elif date_str.isdigit():
            return datetime.datetime(today.year, today.month, int(date_str)).date()
    except ValueError:
        return -1


if __name__ == '__main__':
    print("포털 ID를 입력하세요.(미입력시 환경변수 기본값)")
    ID = input("ID: ")
    if ID.strip() == "":
        ID = None
        PW = None
    else:
        print("포털 PW를 입력하세요.")
        PW = input("PW: ")
    print()

    print("원하는 실습실을 선택하세요.")
    i = 1
    labs = []
    for lab in enums.Lab:
        labs.append(lab)
        print(i, ". ", lab.name, sep="")
        i += 1
    lab = labs[int(input("\n선택: ")) - 1]

    # print("원하는 작업 유형을 선택하세요.")
    # print("1. 저장된 시간표로 자동 입력")
    # print("2. 지정 범위 기록 삭제")
    # act = input("입력: ")

    print("\n날짜 범위를 입력하세요.(yy.mm.dd, mm.dd, dd)")
    while True:
        start_date = input("시작: ")
        end_date = input("끝: ")
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
        if start_date == -1 or end_date == -1:
            print("다시 입력하세요.(yy.mm.dd, mm.dd, dd)")
            continue
        else:
            break

    print("예외 날짜를 입력하세요.(쉼표로 구분, 없으면 엔터)")
    while True:
        except_date = input("예외: ").strip().split(",")
        if not except_date:
            except_date = None
        except_date = [date.strip() for date in except_date if date.strip()]
        except_date = [parse_date(date) for date in except_date]
        if -1 in except_date:
            print("다시 입력하세요.(yy.mm.dd, mm.dd, dd)")
            continue
        else:
            break

    pd.start_and_enter_lab_manage_handling_except(ID, PW)
    lm.manage_lab_at_range_of_date(lab, start_date, end_date, except_date)
