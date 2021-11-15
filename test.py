from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import process_covid_API
from covid_data_handler import schedule_covid_updates
from covid_data_handler import update_covid_data


def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639


def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28'
                                                                                                  '.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544


def test_covid_API_request():
    print(covid_API_request())


def test_process_covid_API():
    print(process_covid_API(covid_API_request()))


def test_schedule_covid_updates():
    schedule_covid_updates(5, update_covid_data)


test_parse_csv_data()
test_process_covid_csv_data()
# test_covid_API_request()
test_process_covid_API()
test_schedule_covid_updates()