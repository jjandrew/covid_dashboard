"""
Tests for the news_data_handling module
"""
from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import update_removed_news
from covid_news_handling import schedule_news_updates
from covid_news_handling import news_update


def test_news_API_request():
    """
    Tests API request can be made
    Tests default values are used
    Tests different terms can be used
    """
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()
    assert news_API_request("Russia China")


def test_update_news():
    """
    Tests update_news returns a value
    """
    assert update_news()
    update_news('test')


def test_update_removed_news():
    """
    Tests an article can be removed from future news searches
    """
    assert update_removed_news("Test Title") == "Test Title"


def test_schedule_news_updates():
    """
    Tests updates for the news can be scheduled
    """
    assert schedule_news_updates(10, 'update test')
    schedule_news_updates(update_interval=10, update_name='update test')


def test_news_update():
    """
    Tests news_update returns an array
    """
    assert type(news_update("test", False, True)) is type([])
