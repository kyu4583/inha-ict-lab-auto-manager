import pytest
import calendar_manager


def test_일반():
    calendar_manager.add_monthly_calendar(5, 2024)
    week_list = calendar_manager.calendar_data[2024][5]['week_list']
    coordinates = calendar_manager.calendar_data[2024][5]['coordinates']
    assert week_list[3][4] == 15
    assert coordinates[15] == [3, 4]


def test_한달에_4주뿐():
    calendar_manager.add_monthly_calendar(2, 1998)
    week_list = calendar_manager.calendar_data[1998][2]['week_list']
    coordinates = calendar_manager.calendar_data[1998][2]['coordinates']
    assert len(week_list) == 6
    assert week_list[5][4] == 0


if __name__ == '__main__':
    pytest.main()
