import calendar
import datetime

class Calendar:
    def __init__(self, week_list, coordinates):
        self.week_list = week_list
        self.coordinates = coordinates

def create_monthly_calendar(month=None, year=None):
    today = datetime.date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    week_list = create_week_list(month, year)
    _, last_day = calendar.monthrange(year, month)
    coordinates = create_coordinates(week_list, last_day)

    return Calendar(week_list, coordinates)
def create_week_list(month, year):

    # 일요일을 한 주의 시작으로 설정
    calendar.setfirstweekday(calendar.SUNDAY)

    # calendar 모듈을 사용하여 해당 월의 달력을 리스트 형태로 가져옴
    cal = calendar.monthcalendar(year, month)

    # 5주가 모두 채워지지 않은 경우 빈 주(리스트)를 추가
    while len(cal) < 5:
        cal.append([0] * 7)

    cal.insert(0, [0] * 7)

    for i in range(len(cal)):
        cal[i] = [0] + cal[i]

    return cal

def create_coordinates(week_list, last_day):
    index_1 = [1, week_list[1].index(1)]
    coordinates = [[0, 0], index_1]

    last_index = index_1
    for i in range(2, last_day + 1):
        if(last_index[1] == 7):
            current_index = [last_index[0] + 1, 1]
        else:
            current_index = [last_index[0], last_index[1] + 1]

        last_index = current_index
        coordinates.append(current_index)

    return coordinates