"""This module will store the general data and functions that need to be accessed by all modules
"""
import sched
import time


scheduler = sched.scheduler(time.time, time.sleep)
local_week_figs = 0
nation_week_figs = 0
nation_hospital_figs = 0
nation_deaths = 0
articles = []
scheduled_events = []


def get_scheduler():
    """Will return the scheduler to the user_interface
    :return: scheduler
    """
    return scheduler


def update_scheduler(updated_s):
    """Will update the scheduler stored in the module

    :param updated_s: Scheduler to be passed in
    """
    global scheduler
    scheduler = updated_s


def get_covid_values() -> tuple:
    """Will return the covid_values to the user interface

    :return: local weekly figures, national weekly figures,
    national hospital figures, national total deaths as a tuple
    """
    return local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths


def set_covid_values(local_figs, national_week_figs, national_hospital_figs, national_deaths):
    """Will set the values for data that needs to be accessed by the user interface

    :param local_figs: local weekly figures may be int or string
    :param national_week_figs: national weekly figures may be int or string
    :param national_hospital_figs: national hospital cases may be int or string
    :param national_deaths: total number of national deaths may be int or string
    """
    global local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths
    local_week_figs = local_figs
    nation_week_figs = national_week_figs
    nation_hospital_figs = national_hospital_figs
    nation_deaths = national_deaths


def get_news_articles() -> list:
    """Function for providing user interface with the stored articles

    :return: Articles
    """
    return articles


def set_news_articles(news_articles: list):
    """Will set the news articles to be accessed by the user interface

    :param news_articles: articles to be set
    """
    global articles
    articles = news_articles


def get_scheduled_events() -> list:
    """This function will return scheduled events for use in all modules

    :return: Scheduled events
    """
    return scheduled_events


def set_scheduled_events(events: list):
    """Will set scheduled events for use in all modules

    :param events: Scheduled events
    """
    global scheduled_events
    scheduled_events = events
