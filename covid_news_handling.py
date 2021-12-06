"""
This module receives articles from the newsapi
It has two functions one for calling API and one for processing the responses
"""
import logging
import requests
from decode_config import decode_config
from shared_data import get_scheduler
from shared_data import update_scheduler
from shared_data import set_news_articles
from shared_data import get_scheduled_events
from shared_data import set_scheduled_events


removed = []


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    """
    Takes in terms to be searched in the API as a string separated by spaces and
    returns an array of the responses received from the various API calls
    :param covid_terms: Takes in a string separated by spaces of terms to be searched for in the API
    :return: Array of the responses received from the various API calls
    """
    base_url = "https://newsapi.org/v2/everything?"
    _, _, _, news_api_key, _, _ = decode_config()
    if news_api_key == "":
        logging.warning("No News API Key Provided")
        return []
    # Splits terms taken in as arguments into an array of the separate terms split by a space
    terms = covid_terms.split(" ")
    responses = []
    # Cycles through the terms given and makes an API request
    for term in terms:
        complete_url = base_url + "q=" + term + "&apiKey=" + news_api_key
        try:
            response = requests.get(complete_url)
            responses.append(response.json())
        except Exception as exception:
            error_message = "Error connection to NewsAPI: " + str(exception)
            logging.warning(error_message)
    return responses


def update_news(test=None):
    """
    Retrieves api responses and loops through the articles in each of the
    responses appending each article to an array.
    :return: articles returned from the various API calls or empty array if no key provided
    """
    # Will check if search terms were provided in the config file
    # need to change 3rd below to retrieve api_key from config file
    _, _, _, _, search_terms, _ = decode_config()
    # Receives api responses from news_API_request function
    if search_terms == "":
        # Will use default values if empty string is used
        api_responses = news_API_request()
    else:
        api_responses = news_API_request(search_terms)
    articles = []
    # Cycles through responses adding each article to an array
    for response in api_responses:
        try:
            for article in response['articles']:
                try:
                    # Checks articles haven't already been removed
                    if article['title'] not in removed:
                        articles.append(article)
                except KeyError:
                    logging.warning("Key Error reading article title from news JSON")
        except KeyError:
            logging.warning("Key Error reading articles from news JSON")
    # Checks if a test is to be carried out
    if test:
        assert api_responses
        assert articles
        assert decode_config()
    return articles


def update_removed_news(title):
    """
    This function will add a removed event to an array so it isn't searched for again
    :param title: The title of the event that is to not be searched for again
    :return: Title for use in testing to make sure procedure ran
    """
    removed.append(title)
    articles = update_news()
    set_news_articles(articles)
    return title


def schedule_news_updates(update_interval, update_name):
    """
    Will carry out the event denoted by update_name after the interval shown by update_interval
    :param update_interval: Time of the update
    :param update_name: Name of the update
    :return: test if test case has been passed in
    """
    # Retrieves a list of scheduled events
    scheduled_events = get_scheduled_events()
    # Checks if the event is to be repeated
    repeat = False
    for event in scheduled_events:
        if event["title"] == update_name:
            repeat = event["repeat"]
    scheduler = get_scheduler()
    # Adds the event to the scheduler
    if repeat:
        scheduler.enter(update_interval, 1, news_update, (update_name, True,))
    else:
        scheduler.enter(update_interval, 1, news_update, (update_name,))
    # Updates the scheduler
    update_scheduler(scheduler)
    if update_interval == 10 and update_name == 'update test':
        assert scheduler
        return "test"


def news_update(update_name, repeat=False, test=False):
    """
    The function called by the scheduler to print the response from news API
    :param update_name: Name of the update to be carried out
    :param repeat: Whether the event is to be repeated
    :return: Used when test case is passed in to make sure program exists
    """
    # Retrieves the scheduled events
    scheduled_events = get_scheduled_events()
    # Checks if event is still in scheduled events
    for event in scheduled_events:
        if event["title"] == update_name:
            # Updates news articles
            articles = update_news()
            set_news_articles(articles)
            # Checks if event is to be repeated
            if repeat:
                scheduler = get_scheduler()
                # Adds event to the scheduler for 24 hours time and updates scheduler
                scheduler.enter(24 * 60 * 60, 1, news_update, (update_name, True,))
                update_scheduler(scheduler)
            else:
                # Removes event from scheduled events if it is not to be repeated
                for scheduled_event in scheduled_events:
                    if scheduled_event["title"] == update_name:
                        scheduled_events.remove(scheduled_event)
                set_scheduled_events(scheduled_events)
    if test:
        return scheduled_events
