"""This module will be used to check that the config file is valid and then return values
"""
import json
import logging


def decode_config(file_name='config.json') -> tuple:
    """This function reads from the config.json file and will return suitable values

    :return: Relevant values retrieved from the json file
    """
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            json_file = json.load(file)
            try:
                location = json_file["location"]
                if location == "":
                    location = "Exeter"
            except KeyError:
                location = "Exeter"
            try:
                location_type = json_file["location_type"]
                if location_type == "":
                    location_type = "ltla"
            except KeyError:
                location_type = "ltla"
            try:
                nation_location = json_file["nation_location"]
                if nation_location == "":
                    nation_location = "England"
            except KeyError:
                nation_location = "England"
            try:
                news_api_key = json_file["news_api_key"]
            except KeyError:
                logging.error("No key provided in config file")
                news_api_key = ""
            try:
                search_terms = json_file["search_terms"]
            except KeyError:
                search_terms = ""
            try:
                image_name = json_file["image_name"]
                if image_name == "":
                    image_name = 'covid_image.jpeg'
            except KeyError:
                image_name = 'covid_image.jpeg'
    except FileNotFoundError:
        logging.error("No config.json File Provided")
        return "Exeter", "ltla", "England", "", "", "covid_image.jpeg"
    return location, location_type, nation_location, news_api_key, search_terms, image_name
