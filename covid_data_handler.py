"""
This Module processes the data received in the 'nation_2021-10-28.csv' file
"""


def parse_csv_data(csv_filename):
    """
    This function will read from the 'nation_2021-10-28' file and return a list of strings corresponding to each
    line of the csv file.
    :param csv_filename:
    :return: List[str] of each line of the csv file
    """
    data = []
    # Iterates through the file and strips '\n' from each line before adding the line as a string to the data list
    with open(csv_filename, 'r') as f:
        for row in f:
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
