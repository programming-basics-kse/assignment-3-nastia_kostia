import argparse
import csv


def parse_command_line():
    parser = argparse.ArgumentParser(
        prog='Olympics',
        description='Top 10 medalists from given country'
    )

    parser.add_argument('filename', help='Path to the data file')
    parser.add_argument('-m', '--medals', nargs=2, help='country abbreviation and year')
    return parser.parse_args()


def read_data_from_file(filename: str):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        return [row for row in reader]


def is_country_and_year_valid(data, country: str, year: str):
    for row in data:
        if not row['Team'] == country and not row['NOC'] == country:
            continue
        if not row['Year'] == year:
            continue
        return True
    return False


def get_medals_by_country_year(data, country: str, year: str):
    pass


def print_medals(file_name: str = None):
    pass


if __name__ == '__main__':
    args = parse_command_line()
    data = read_data_from_file(args.filename)
    if not is_country_and_year_valid(data, args.medals[0], args.medals[1]):
        print("Not valid country or there was no olympiad in given year")
        exit()
    medals = get_medals_by_country_year(data, args.medals[0], args.medals[1])
    print_medals(medals)
