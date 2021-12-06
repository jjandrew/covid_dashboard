from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import update_removed_news
from covid_news_handling import schedule_news_updates
from covid_news_handling import news_update


def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()
    assert news_API_request("Russia China")


def test_update_news():
    assert update_news()
    update_news('test')


def test_update_removed_news():
    assert update_removed_news("Test Title") == "Test Title"


def test_schedule_news_updates():
    assert schedule_news_updates(10, 'update test')
    schedule_news_updates(update_interval=10, update_name='update test')


def test_news_update():
    assert type(news_update("test", False, True)) is type([])
