"""
This Module processes the data received in the 'nation_2021-10-28.csv' file
and receives information from the public health England API
"""
import sched
import time
from uk_covid19 import Cov19API


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
    with open(csv_filename, 'r', encoding="utf-8") as file:
        for row in file:
            data.append(row.rstrip())
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
    api = Cov19API(filters=location_entry, structure=data_required)
    response = api.get_json()
    return response


def process_covid_API(covid_json):
    """
    Retrieves weekly cases, hospital cases and total deaths from the json
    :param covid_json: Data retrieved from the API call
    :return: weekly cases, hospital cases, total deaths
    """
    covid_json = covid_json['data']
    # calculates weekly cases by summing last 7 entries exluding most recent entry
    week_cases = 0
    for i in range(2, 9):
        week_cases += covid_json[i]['newCasesBySpecimenDate']
    # calculates hospital cases by reading value in JSON file
    hospital_cases = covid_json[1]['hospitalCases']
    # iterates through json until an entry for cumulative deaths is found
    count = 1
    while covid_json[count]['cumDailyNsoDeathsByDeathDate'] is None and count < len(covid_json)-1:
        count += 1
    if count == len(covid_json):
        total_deaths = None
    else:
        total_deaths = covid_json[count]['cumDailyNsoDeathsByDeathDate']
    return week_cases, hospital_cases, total_deaths


def schedule_covid_updates(update_interval, update_name):
    """
    Will carry out the function denoted by update_name after the interval shown by update_interval
    :param update_interval:
    :param update_name:
    :return:
    """
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(update_interval, 1, update_name)
    scheduler.run()


def update_covid_data():
    """
    The function called by the scheduler to print the covid data from the API
    """
    # print(process_covid_API(covid_API_request()))
    return
