import calendar
import datetime

calendar_data = {}


# 특정 년-월의 달력을 생성해 달력 딕셔너리에 추가
def add_monthly_calendar(month=None, year=None):
    today = datetime.date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    if calendar_data.get(year) is None:

        # 해당 년 딕셔너리가 없으면 추가
        calendar_data[year] = {}

    if calendar_data.get(year).get(month) is None:

        # 해당 년-월 데이터가 없으면 만들어서 추가
        week_list = create_week_list(month, year)
        _, last_day = calendar.monthrange(year, month)
        coordinates = create_coordinates(week_list, last_day)
        calendar_data[year][month] = {'week_list': week_list, 'coordinates': coordinates}

    else:
        pass


def create_week_list(month, year):
    # 일요일을 한 주의 시작으로 설정
    calendar.setfirstweekday(calendar.SUNDAY)

    # calendar 모듈을 사용하여 해당 월의 달력을 리스트 형태로 가져옴
    week_list = calendar.monthcalendar(year, month)

    # 5주가 모두 채워지지 않은 경우 빈 주(리스트)를 추가
    while len(week_list) < 5:
        week_list.append([0] * 7)

    # 행/열의 인덱스가 1부터 세어지도록, 빈 요소를 인덱스 0의 자리마다 추가
    week_list.insert(0, [0] * 7)
    for i in range(len(week_list)):
        week_list[i] = [0] + week_list[i]

    return week_list


def create_coordinates(week_list, last_day):

    # 1일의 인덱스
    index_1 = [1, week_list[1].index(1)]

    # 각 일(=인덱스)의 좌표를 기록하는 리스트
    coordinates = [[0, 0], index_1]

    last_index = index_1
    for i in range(2, last_day + 1):

        # 이전 좌표가 주의 마지막일(토요일)이라면 좌표가 다음주로 넘어감
        if (last_index[1] == 7):
            current_index = [last_index[0] + 1, 1]
        else:
            current_index = [last_index[0], last_index[1] + 1]

        last_index = current_index
        coordinates.append(current_index)

    return coordinates
