import unittest
import calendar_manager


class TestMyFunction(unittest.TestCase):
    def test_일반(self):
        calendar_manager.add_monthly_calendar(5, 2024)
        week_list = calendar_manager.calendar_data[2024][5]['week_list']
        coordinates = calendar_manager.calendar_data[2024][5]['coordinates']
        self.assertEqual(week_list[3][4], 15)
        self.assertEqual(coordinates[15], [3, 4])

    def test_한달에_4주뿐(self):
        calendar_manager.add_monthly_calendar(2, 1998)
        week_list = calendar_manager.calendar_data[1998][2]['week_list']
        coordinates = calendar_manager.calendar_data[1998][2]['coordinates']
        self.assertEqual(len(week_list), 6)
        self.assertEqual(week_list[5][4], 0)

if __name__ == '__main__':
    unittest.main()
