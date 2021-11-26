from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import schedule_covid_updates
from covid_data_handler import update_covid_data
from tests import test_covid_data_handler
from tests import test_news_data_handling


def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639


def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28'
                                                                                                  '.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544


def test_schedule_covid_updates():
    schedule_covid_updates(5, update_covid_data)


test_parse_csv_data()
print('Test 1 finished')
test_process_covid_csv_data()
print('Test 2 finished')
test_schedule_covid_updates()
print('Test 3 finished')
test_covid_data_handler.test_process_covid_csv_data()
print('Test 4 finished')
test_covid_data_handler.test_parse_csv_data()
print('Test 5 finished')
test_covid_data_handler.test_covid_API_request()
print('Test 6 finished')
try:
    test_covid_data_handler.test_schedule_covid_updates()
except AssertionError:
    print("Test 7 failed")
except TypeError:
    print("Test 7 failed")
print('Test 7 finished')
try:
    test_news_data_handling.test_update_news()
except TypeError:
    print("Test 8 failed")
print('Test 8 finished')
test_news_data_handling.test_news_API_request()
print('Test 9 finished')