"""
This module receives articles from the newsapi
It has two functions one for calling API and one for processing the responses
"""
import requests
from keys import get_newsapi_key


def news_API_request(covid_terms="Covid COVID-19 coronavirus"):
    """
    Takes in terms to be searched in the API as a string separated by spaces and
    returns an array of the responses received from the various API calls
    :param covid_terms: Takes in a string separated by spaces of terms to be searched for in the API
    :return: Array of the responses received from the various API calls
    """

    base_url = "https://newsapi.org/v2/everything?"
    api_key = get_newsapi_key()
    terms = covid_terms.split(" ")
    responses = []
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
    api_responses = news_API_request()
    articles = []
    for response in api_responses:
        for article in response['articles']:
            articles.append(article)
    return articles


update_news()
