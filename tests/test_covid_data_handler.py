"""
Tests for covid_data_handler to run using pytest
"""
from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import process_covid_API
from covid_data_handler import schedule_covid_updates
from covid_data_handler import update_covid_data
from covid_data_handler import get_starting_data


def test_parse_csv_data():
    """
    Tests the parce_csv_data function returns the correct values
    """
    assert parse_csv_data('nation_2021-10-28.csv')
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639
    assert parse_csv_data('abc.csv') == []


def test_process_covid_csv_data():
    """
    Tests the process_covid_csv_data function can handle information correctly and deal with errors
    """
    assert process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    last7days_cases, current_hospital_cases, total_deaths = \
        process_covid_csv_data(parse_csv_data(
            'nation_2021-10-28.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544
    assert process_covid_csv_data(parse_csv_data('abc.csv')) == ("Error", "Error", "Error")


def test_covid_API_request():
    """
    Tests covid_API_request function can make a request and return a dictionary
    :return:
    """
    assert covid_API_request()
    data = covid_API_request()
    assert isinstance(data, dict)
    assert covid_API_request("abc", "Nation")


def test_process_covid_API():
    """
    Tests the process_covid_API function can deal with empty arguments and
    argument of incorrect form
    :return:
    """
    assert process_covid_API({}) == ("Error", "Error", "Error")
    test_data = {"data": {'Test': 0, "Test1": 1}}
    assert process_covid_API(test_data) == ("Error", "Error", "Error")
    test_data_1 = {"data": [{"Test": 0, "Test1": 1, "Test2": 2},
                            {"Test": 0, "Test1": 1, "Test2": 2},
                            {"Test": 0, "Test1": 1, "Test2": 2}]}
    assert process_covid_API(test_data_1) == ("Error", "Error", "Error")


def test_schedule_covid_updates():
    """
    Tests updates on covid data can be scheduled
    """
    assert schedule_covid_updates(10, 'update test')
    schedule_covid_updates(update_interval=10, update_name='update test')


def test_update_covid_data():
    """
    Tests no scheduled events are present when test is passed in
    """
    assert update_covid_data("test") == "No scheduled events"


def test_get_starting_data():
    """
    Tests the correct starting data is returned even when API calls are not possible
    """
    assert get_starting_data("test1") == ("Error", "Error", "National Hospital Cases: Error",
                                          "National Total Deaths: Error")
    assert get_starting_data() == "Complete"
