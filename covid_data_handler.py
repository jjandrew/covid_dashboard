"""
This Module processes the data received in the 'nation_2021-10-28.csv' file
"""


def parse_csv_data(csv_filename):
    """
    This function will read from the 'nation_2021-10-28' file and return a list of strings corresponding to each
    line of the csv file.
    :param csv_filename:
    :return: List[str]
    """
    data = []
    with open(csv_filename, 'r') as f:
        for row in f:
            data.append(row.rstrip())
    return data


def process_covid_csv_data(covid_csv_data):
    week_cases = 0
    for i in range(3, 10):
        week_cases += int(covid_csv_data[i].split(',')[6])
    hospital_cases = 0
    total_deaths = 1
    return week_cases, hospital_cases, total_deaths
