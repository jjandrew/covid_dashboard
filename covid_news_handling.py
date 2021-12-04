"""
This module receives articles from the newsapi
It has two functions one for calling API and one for processing the responses
"""
import logging
import requests
from keys import get_newsapi_key
from decode_config import decode_config
from time_conversions import hhmm_to_secs
from shared_data import get_scheduler
from shared_data import update_scheduler
from shared_data import set_news_articles


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
        logging.warning("No API Key Provided")
        return []
    api_key = get_newsapi_key()
    # Splits terms taken in as arguments into an array of the separate terms split by a space
    terms = covid_terms.split(" ")
    responses = []
    # Cycles through the terms given and makes an API request
    for term in terms:
        complete_url = base_url + "q=" + term + "&apiKey=" + api_key
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
    """
    removed.append(title)


def schedule_news_updates(update_interval, update_name):
    """
    Will carry out the event denoted by update_name after the interval shown by update_interval
    :param update_interval: Time of the update
    :param update_name: Name of the update
    :return:
    """
    update_interval = hhmm_to_secs(update_interval)
    scheduler = get_scheduler()
    job = scheduler.enter(5, 1, news_update, ())
    update_scheduler(scheduler)
    return scheduler


def news_update():
    """
    The function called by the scheduler to print the response from news API
    """
    articles = update_news()
    set_news_articles(articles)
