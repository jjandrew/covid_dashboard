from shared_data import get_scheduler
from shared_data import update_scheduler
from shared_data import get_covid_values
from shared_data import set_covid_values
from shared_data import get_news_articles
from shared_data import set_news_articles
from shared_data import get_scheduled_events
from shared_data import set_scheduled_events


def test_get_scheduler():
    assert get_scheduler()


def test_update_scheduler():
    scheduler = get_scheduler()
    update_scheduler(scheduler)
    assert get_scheduler() == scheduler


def test_get_covid_values():
    assert get_covid_values()
    assert len(get_covid_values()) == 4


def test_set_covid_values():
    local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths = get_covid_values()
    set_covid_values(local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths)
    assert get_covid_values() == (local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths)


def test_get_news_articles():
    assert type(get_news_articles()) is type([])


def test_set_news_articles():
    articles = get_news_articles()
    set_news_articles(articles)
    assert get_news_articles() == articles


def test_get_scheduled_events():
    assert type(get_scheduled_events()) is type([])


def test_set_scheduled_events():
    events = get_scheduled_events()
    set_scheduled_events(events)
    assert get_scheduled_events() == events


test_get_news_articles()
