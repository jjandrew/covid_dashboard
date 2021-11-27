import json


def decode_config():
    """
    This function reads from the config.json file and will return suitable values
    :return: Relevant values retrieved from the json file
    """
    file = open('config.json')
    json_file = json.load(file)
    try:
        location = json_file["location"]
    except KeyError:
        location = None
    try:
        location_type = json_file["location_type"]
    except KeyError:
        location_type = None
    try:
        news_api_key = json_file["news_api_key"]
    except KeyError:
        print("No key provided")
        news_api_key = None
    try:
        search_terms = json_file["search_terms"]
    except KeyError:
        search_terms = ""
    try:
        image_name = json_file["image_name"]
    except KeyError:
        image_name = 'covid_image.jpeg'
    return location, location_type, news_api_key, search_terms, image_name
