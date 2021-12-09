"""Tests for the shared_data module to be run using Pytest
"""
from shared_data import get_scheduler
from shared_data import update_scheduler
from shared_data import get_covid_values
from shared_data import set_covid_values
from shared_data import get_news_articles
from shared_data import set_news_articles
from shared_data import get_scheduled_events
from shared_data import set_scheduled_events


def test_get_scheduler():
    """Tests that a scheduler is returned
    """
    assert get_scheduler()


def test_update_scheduler():
    """Tests that the scheduler can be updated and then retrieved
    """
    scheduler = get_scheduler()
    update_scheduler(scheduler)
    assert get_scheduler() == scheduler


def test_get_covid_values():
    """Tests that 4 covid values are returned when get_covid_values is called
    """
    assert get_covid_values()
    assert len(get_covid_values()) == 4


def test_set_covid_values():
    """Tests covid_values can be set and then retrieved
    """
    local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths = get_covid_values()
    set_covid_values(local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths)
    assert get_covid_values() == (local_week_figs, nation_week_figs, nation_hospital_figs,
                                  nation_deaths)


def test_get_news_articles():
    """Tests news articles are returned as a list
    """
    data = get_news_articles()
    assert isinstance(data, list)


def test_set_news_articles():
    """Tests news articles can be set and then retrieved
    """
    articles = get_news_articles()
    set_news_articles(articles)
    assert get_news_articles() == articles


def test_get_scheduled_events():
    """Tests get_scheduled_events returns a list
    """
    data = get_scheduled_events()
    assert isinstance(data, list)


def test_set_scheduled_events():
    """Tests scheduled events can be set and then retrieved
    """
    events = get_scheduled_events()
    set_scheduled_events(events)
    assert get_scheduled_events() == events
