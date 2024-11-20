import argparse
import csv


def parse_command_line():
    parser = argparse.ArgumentParser(
        prog='Olympics',
        description='Top 10 medalists from given country'
    )

    parser.add_argument('filename', help='Path to the data file')
    parser.add_argument('-m', '--medals', nargs=2, required=True, help='country abbreviation and year')
    parser.add_argument('-o', '--output', help='The name of the output file')
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
    medals = []
    for row in data:
        if not row['Team'] == country and not row['NOC'] == country:
            continue
        if not row['Year'] == year or row['Medal'] == 'NA':
            continue
        medals.append({'Name': row['Name'], 'Sport': row['Sport'], 'Medal': row['Medal']})
    return medals  


def print_medals(medals, file_name: str = None):
    if len(medals) < 10:
        print("Country has less then 10 medals")
        return
    table_header = "{:30s} | \t {:25s} |\t {}\n".format("Name", "Sport", "Medal")
    print(table_header)
    for medal in medals[:10]:
        print(f"{medal['Name']:30s} |\t {medal['Sport']:25s} |\t {medal['Medal']}")


if __name__ == '__main__':
    args = parse_command_line()
    data = read_data_from_file(args.filename)
    if not is_country_and_year_valid(data, args.medals[0], args.medals[1]):
        print("Not valid country or there was no olympiad in given year")
        exit()
    medals = get_medals_by_country_year(data, args.medals[0], args.medals[1])
    print_medals(medals)
