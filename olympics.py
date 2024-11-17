arguments = {
    'input_filename': '',
    'output_filename': '',
    'country': '',
    'year': ''
}

def parse_command_line():
    #get command line arguments
    pass

def read_data_from_file(filename: str):
    #read data from file and return as a dictionnary
    pass

def is_country_and_year_valid(country: str, year: str):
    #check whether arguments country and year exists in a data sample 
    pass

def get_medals_by_country_year(country: str, year: str):
    pass

def print_medals(file_name: str = None):
    pass

if __name__ == '__main__':
    parse_command_line()
    data = read_data_from_file(arguments['input_filename'])
    if not is_country_and_year_valid(arguments['country'], arguments['year']):
        print("Not valid country or there was no olympiad in given year")
        exit()
    medals = get_medals_by_country_year(arguments['country'], arguments['year'])
    print_medals(medals)

