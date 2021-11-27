"""
This module receives articles from the newsapi
It has two functions one for calling API and one for processing the responses
"""
import requests
from keys import get_newsapi_key
from decode_config import decode_config


removed = []


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    """
    Takes in terms to be searched in the API as a string separated by spaces and
    returns an array of the responses received from the various API calls
    :param covid_terms: Takes in a string separated by spaces of terms to be searched for in the API
    :return: Array of the responses received from the various API calls
    """
    base_url = "https://newsapi.org/v2/everything?"
    api_key = get_newsapi_key()
    # Splits terms taken in as arguments into an array of the separate terms split by a space
    terms = covid_terms.split(" ")
    responses = []
    # Cycles through the terms given and makes an API request
    for term in terms:
        complete_url = base_url + "q=" + term + "&apiKey=" + api_key
        response = requests.get(complete_url)
        responses.append(response.json())
    return responses


def update_news():
    """
    Retrieves api responses and loops through the articles in each of the
    responses appending each article to an array.
    :return: articles returned from the various API calls
    """
    # Will check if search terms were provided in the config file
    # need to change 3rd below to retrieve api_key from config file
    _, _, _, search_terms, _ = decode_config()
    api_responses = []
    # Receives api responses from news_API_request function
    if search_terms == "":
        # Will use default values if empty string is used
        api_responses = news_API_request()
    else:
        api_responses = news_API_request(search_terms)
    articles = []
    # Cycles through responses adding each article to an array
    for response in api_responses:
        for article in response['articles']:
            # Checks articles haven't already been removed
            if article not in removed:
                articles.append(article)
    return articles
