import argparse
import csv
import parser  


def parse_command_line():
    parser = argparse.ArgumentParser(
        prog='Olympics',
        description='Top 10 medalists from given country'
    )

    parser.add_argument('filename', help='Path to the data file')
    parser.add_argument('-m', '--medals', nargs=2, help='country abbreviation and year')
    parser.add_argument('-o', '--output', help='The name of the output file')
    parser.add_argument('-i', '--interactive', action='store_const', const=True, help='Enters interactive mode to access data for given country')
    return parser.parse_args()


def read_data_from_file(filename: str):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        return [row for row in reader]


if __name__ == '__main__':
    args = parse_command_line()
    data = read_data_from_file(args.filename)
    is_interactive = False
    if args.medals:
        parser = parser.Top10Medalists(data, args.medals)
    elif args.interactive:
        parser = parser.Interactive(data)
        is_interactive = True
    elif args.total:
        parser = parser.Total(data, args.medals)
    elif args.overall:
        parser = parser.Overall(data, args.medals)

    if is_interactive:
        while(1):
            country = input("Enter country name or code: ")
            if country == 'q':
                exit()
            parser.parse_data(country)
            parser.print_data()

    if not parser.check_data():
        exit()
    parser.parse_data()
    parser.print_data(args.output)
