"""
This Module processes the data received in the 'nation_2021-10-28.csv' file
and receives information from the public health England API
"""
import logging
import json
from uk_covid19 import Cov19API
from decode_config import decode_config
from shared_data import get_scheduler
from shared_data import update_scheduler
from shared_data import set_covid_values
from shared_data import get_scheduled_events
from shared_data import set_scheduled_events


def parse_csv_data(csv_filename):
    """
    This function will read from the 'nation_2021-10-28' file and return a list of strings
    corresponding to each line of the csv file.
    :param csv_filename:
    :return: List[str] of each line of the csv file
    """
    data = []
    # Iterates through the file and strips '\n' from each line before
    # adding the line as a string to the data list
    try:
        with open(csv_filename, 'r', encoding="utf-8") as file:
            for row in file:
                data.append(row.rstrip())
    except FileNotFoundError:
        logging.warning("Invalid csv file name")
        data = []
    return data


def process_covid_csv_data(covid_csv_data):
    """
    Takes in csv data file as input and calculates:
        Cases for last week excluding most recent value as is incomplete
        Hospital cases
        Cumulative Deaths as up to date as file allows
    :param covid_csv_data:
    :return: weekly cases, hospital cases, cumulative deaths as integers
    """
    if covid_csv_data == []:
        return "Error", "Error", "Error"
    # calculates weekly cases by summing last 7 entries
    week_cases = 0
    for i in range(3, 10):
        week_cases += int(covid_csv_data[i].split(',')[6])
    # calculates hospital cases by reading last entry to csv file
    hospital_cases = int(covid_csv_data[1].split(',')[5])
    # iterates through csv file until an entry for cumulative deaths is found
    count = 1
    while covid_csv_data[count].split(',')[4] == '':
        count += 1
    total_deaths = int(covid_csv_data[count].split(',')[4])
    return week_cases, hospital_cases, total_deaths


def covid_API_request(location="Exeter", location_type="ltla"):
    """
    Retrieves COVID data from the public health England API
    Will be able to search based on the location and location_type passed in as parameters
    :param location: location to be searched for in API
    :param location_type: type of entry location is
    :return: Data returned from PHE API in json format
    """
    location_entry = [
        'areaName='+location,
        'areaType='+location_type
    ]
    data_required = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }
    response = {}
    # Tries to retrieve information from the Covid API
    try:
        api = Cov19API(filters=location_entry, structure=data_required)
        response = api.get_json()
    except Exception as exception:
        error_message = "Error connection to Covid API: " + str(exception)
        logging.warning(error_message)
    return response


def process_covid_API(covid_json):
    """
    Retrieves weekly cases, hospital cases and total deaths from the json
    :param covid_json: Data retrieved from the API call
    :return: weekly cases, hospital cases, total deaths
    """
    try:
        covid_json = covid_json['data']
    except KeyError:
        logging.warning("Incorrect information in config file: Covid API error")
        return "Error", "Error", "Error"
    # calculates weekly cases by summing last 7 entries excluding most recent entry
    week_cases = 0
    try:
        for i in range(2, 9):
            try:
                week_cases += covid_json[i]['newCasesBySpecimenDate']
            except KeyError:
                logging.warning("Key Error reading new cases by specimen date")
                week_cases = "Error"
                break
    except IndexError:
        logging.warning("Index error reading covid JSON")
        week_cases = "Error"
    # calculates hospital cases by reading value in JSON file
    try:
        hospital_cases = covid_json[1]['hospitalCases']
    except KeyError:
        hospital_cases = "Error"
        logging.warning("Key error reading hospital cases from JSON")
    except IndexError:
        hospital_cases = "Error"
        logging.warning("Index error reading hospital cases from JSON: Probably due to invalid API call")
    # iterates through json until an entry for cumulative deaths is found
    count = 1
    try:
        while covid_json[count]['cumDailyNsoDeathsByDeathDate'] is None and \
                count < len(covid_json)-1:
            count += 1
    except KeyError:
        logging.warning("Key Error reading cumulative numbers of deaths")
    except IndexError:
        logging.warning("Index Error reading cumulative numbers of deaths: Probably due to invalid API call")
    if count == len(covid_json):
        total_deaths = "Error"
    else:
        try:
            total_deaths = covid_json[count]['cumDailyNsoDeathsByDeathDate']
        except KeyError:
            total_deaths = "Error"
            logging.info("Key Error reading cumulative numbers of deaths")
        except IndexError:
            total_deaths = "Error"
            logging.info("Index Error reading cumulative numbers of deaths: Probably due to invalid API call")
    return week_cases, hospital_cases, total_deaths


def schedule_covid_updates(update_interval, update_name):
    """
    Will carry out the event denoted by update_name after the interval shown by update_interval
    :param update_interval: Time of the update
    :param update_name: Name of the update
    :return: test if test case is passed in
    """
    # Retrieves events that are currently scheduled
    scheduled_events = get_scheduled_events()
    repeat = False
    # Checks if the event is to be repeated or not
    for event in scheduled_events:
        if event["title"] == update_name:
            repeat = event["repeat"]
    # Will schedule the event to occur at the given interval
    scheduler = get_scheduler()
    if repeat:
        scheduler.enter(update_interval, 1, update_covid_data, (update_name, True,))
    else:
        scheduler.enter(update_interval, 1, update_covid_data, (update_name,))
    # Updates the general scheduler
    update_scheduler(scheduler)
    if update_interval == 10 and update_name == 'update test':
        assert scheduler
        return "test"


def update_covid_data(update_name, repeat=False):
    """
    The function called by the scheduler to print the covid data from the API
    :param update_name: Name of the update to be carried out
    :param repeat: Whether or not the update is to be repeated
    """
    scheduled_events = get_scheduled_events()
    # Checks if event is already present
    for event in scheduled_events:
        if event["title"] == update_name:
            # If present it will carry out the function
            # Will retrieve data from the config file
            location, location_type, nation_location, _, _, _ = decode_config()
            # Will retrieve local covid data
            if location == "" or location_type == "":
                local_week_figs, _, _ = process_covid_API(covid_API_request())
            else:
                local_week_figs, _, _ = process_covid_API(covid_API_request(location,
                                                                            location_type))
            # will retrieve national covid data
            if nation_location == "":
                nation_location = "England"
            nation_week_figs, nation_hospital_figs, nation_deaths = \
                process_covid_API(covid_API_request(nation_location, "nation"))
            nation_hospital_figs = "National Hospital Cases: " + str(nation_hospital_figs)
            nation_deaths = "National Total Deaths: " + str(nation_deaths)
            # Will set values from covid_api_calls so the user interface can be updated
            set_covid_values(local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths)
            # Will check if the event is to be repeated
            if repeat:
                scheduler = get_scheduler()
                scheduler.enter(24*60*60, 1, update_covid_data, (update_name, True,))
                update_scheduler(scheduler)
            else:
                # Will automatically remove the event from the scheduled events when carried out
                for scheduled_event in scheduled_events:
                    if scheduled_event["title"] == update_name and \
                            scheduled_event["to_update"] == 'both':
                        break
                    if scheduled_event["title"] == update_name:
                        scheduled_events.remove(event)
                        set_scheduled_events(scheduled_events)
    test_statement = "Complete"
    if not scheduled_events:
        test_statement = "No scheduled events"
    return test_statement


def get_starting_data(test=""):
    """
    Function to retrieve the starting values for the user interface
    """
    # Retrieves data from the config files for the API call
    location, location_type, nation_location, _, _, _ = decode_config()
    if test == 'test1':
        file = open('test.json')
        json_file = json.load(file)
        location = json_file['location']
        location_type = json_file["location_type"]
        nation_location = json_file["nation_location"]
    # Will retrieve the local covid data
    if location == "" or location_type == "":
        local_week_figs, _, _ = process_covid_API(covid_API_request())
    else:
        local_week_figs, _, _ = process_covid_API(covid_API_request(location, location_type))
    # Will retrieve the national covid data
    if nation_location == "":
        nation_location = "England"
    nation_week_figs, nation_hospital_figs, nation_deaths = process_covid_API(covid_API_request
                                                                              (nation_location,
                                                                               "nation"))
    nation_hospital_figs = "National Hospital Cases: " + str(nation_hospital_figs)
    nation_deaths = "National Total Deaths: " + str(nation_deaths)
    # Will set covid values so that the user interface can be updated
    set_covid_values(local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths)
    if test == "test1":
        return local_week_figs, nation_week_figs, nation_hospital_figs, nation_deaths
    else:
        return "Complete"
