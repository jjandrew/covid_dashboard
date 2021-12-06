from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import process_covid_API
from covid_data_handler import schedule_covid_updates


def test_parse_csv_data():
    assert parse_csv_data('nation_2021-10-28.csv')
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639
    assert parse_csv_data('abc.csv') == []


def test_process_covid_csv_data():
    assert process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    last7days_cases, current_hospital_cases, total_deaths = \
        process_covid_csv_data(parse_csv_data(
            'nation_2021-10-28.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544
    assert process_covid_csv_data(parse_csv_data('abc.csv')) == ("Error", "Error", "Error")


def test_covid_API_request():
    assert covid_API_request()
    data = covid_API_request()
    assert isinstance(data, dict)
    assert covid_API_request("abc", "Nation")


def test_process_covid_API():
    assert process_covid_API({}) == ("Error", "Error", "Error")
    test_data = {"data": {'Test': 0, "Test1": 1}}
    assert process_covid_API(test_data) == ("Error", "Error", "Error")
    test_data_1 = {"data": [{"Test": 0, "Test1": 1, "Test2": 2},
                            {"Test": 0, "Test1": 1, "Test2": 2},
                            {"Test": 0, "Test1": 1, "Test2": 2}]}
    assert process_covid_API(test_data) == ("Error", "Error", "Error")


def test_schedule_covid_updates():
    assert schedule_covid_updates(10, 'update test')
    schedule_covid_updates(update_interval=10, update_name='update test')
