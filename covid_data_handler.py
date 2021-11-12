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
            data.append(row)
        return data
