import json


def decode_config(file_name='config.json'):
    """
    This function reads from the config.json file and will return suitable values
    :return: Relevant values retrieved from the json file
    """
    file = open(file_name)
    json_file = json.load(file)
    try:
        location = json_file["location"]
    except KeyError:
        location = ""
    try:
        location_type = json_file["location_type"]
    except KeyError:
        location_type = ""
    try:
        nation_location = json_file["nation_location"]
    except KeyError:
        nation_location = ""
    try:
        news_api_key = json_file["news_api_key"]
    except KeyError:
        print("Error: No key provided in config file")
        news_api_key = ""
    try:
        search_terms = json_file["search_terms"]
    except KeyError:
        search_terms = ""
    try:
        image_name = json_file["image_name"]
    except KeyError:
        image_name = 'covid_image.jpeg'
    return location, location_type, nation_location, news_api_key, search_terms, image_name
