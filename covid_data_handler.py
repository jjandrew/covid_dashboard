def parse_csv_data(csv_filename):
    data = []
    with open (csv_filename, 'r') as f:
        for row in f:
            data.append(row)
        return data