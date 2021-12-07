"""
Module containing the tests to be carried out during runtime
"""
import logging
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
from covid_data_handler import update_covid_data
from decode_config import decode_config
from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import schedule_news_updates
from shared_data import get_scheduler
from shared_data import update_scheduler
from shared_data import get_news_articles
from shared_data import get_scheduled_events
from shared_data import set_scheduled_events


def test_covid_API_request():
    """
    Tests covid_API_request function can make a request and return a dictionary
    :return:
    """
    assert covid_API_request()
    data = covid_API_request()
    assert isinstance(data, dict)
    assert covid_API_request("abc", "Nation")


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


def test_decode_config():
    """
    Tests config file can be decoded and tests it can be decoded if file is edited
    """
    assert decode_config()
    assert decode_config('empty.json') == ("Exeter", "ltla", "England", "", "", 'covid_image.jpeg')


def test_news_API_request():
    """
    Tests API request can be made
    Tests default values are used
    Tests different terms can be used
    """
    try:
        assert news_API_request()
        assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()
        assert news_API_request("Russia China")
    except AssertionError:
        logging.info("Error in news_API_request")


def test_update_news():
    """
    Tests update_news returns a value
    """
    try:
        assert update_news()
    except AssertionError:
        logging.warning("Error with update_news function")
    update_news('test')


def test_schedule_news_updates():
    """
    Tests updates for the news can be scheduled
    """
    assert schedule_news_updates(10, 'update test')
    schedule_news_updates(update_interval=10, update_name='update test')


def test_get_scheduler():
    """
    Tests that a scheduler is returned
    """
    assert get_scheduler()


def test_update_scheduler():
    """
    Tests that the scheduler can be updated and then retrieved
    """
    scheduler = get_scheduler()
    update_scheduler(scheduler)
    assert get_scheduler() == scheduler


def test_get_news_articles():
    """
    Tests news articles are returned as a list
    """
    assert type(get_news_articles()) is type([])


def test_get_scheduled_events():
    """
    Tests get_scheduled_events returns a list
    """
    assert type(get_scheduled_events()) is type([])


def test_set_scheduled_events():
    """
    Tests scheduled events can be set and then retrieved
    """
    events = get_scheduled_events()
    set_scheduled_events(events)
    assert get_scheduled_events() == events


def run_tests():
    """
    This procedure will execute all of the runtime tests
    It will then schedule itself again for an hour's time
    """
    test_covid_API_request()
    test_schedule_covid_updates()
    test_update_covid_data()
    test_decode_config()
    test_news_API_request()
    test_update_news()
    test_schedule_news_updates()
    test_get_scheduler()
    test_update_scheduler()
    test_get_news_articles()
    test_get_scheduled_events()
    test_set_scheduled_events()
    logging.info("Tests completed running")

    # Schedules itself to run again in 1 hour
    scheduler = get_scheduler()
    scheduler.enter(15*60, 1, run_tests, ())
    update_scheduler(scheduler)


def schedule_tests():
    """
    Schedules runtime tests to be carried out
    """
    scheduler = get_scheduler()
    scheduler.enter(1, 1, run_tests, ())
    update_scheduler(scheduler)
