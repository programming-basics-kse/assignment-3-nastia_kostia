
class Parser:
    def __init__(self, data, outputfile=None):
        self.data = data
        self.outputfile = outputfile

    def check_data(self):
        pass

    def parse_data(self):
        pass

    def print_data(self, file_name=None):
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.table_header)
                file.write(self.table)
                print(f'Results written to "{file_name}"')
        else:
            print(self.table_header)
            print(self.table)

class Top10Medalists(Parser):
    def __init__(self, data, args):
        self.data = data
        self.country = args[0]
        self.year = args[1]

    def check_data(self):
        for row in self.data:
            if not row['Team'] == self.country and not row['NOC'] == self.country:
                continue
            if not row['Year'] == self.year:
                continue
            return True
        print("Not valid country or there was no olympiad in given year")
        return False

    def parse_data(self):
        self.medals = []
        for row in self.data:
            if not row['Team'] == self.country and not row['NOC'] == self.country:
                continue
            if not row['Year'] == self.year or row['Medal'] == 'NA':
                continue
            self.medals.append({'Name': row['Name'], 'Sport': row['Sport'], 'Medal': row['Medal']})

        if len(self.medals) < 10:
            print("Country has less then 10 medals")
            return

        self.table_header = "{:30s} | \t {:25s} |\t {}\n".format("Name", "Sport", "Medal")
        self.table = ""
        for medal in self.medals[:10]:
            self.table += f"{medal['Name']:30s} |\t {medal['Sport']:25s} |\t {medal['Medal']}\n"

        return self.medals
    
class Total(Parser):
    def __init__(self, data, args):
        self.data = data
        self.year = args

    def check_data(self):
        pass
    
    def parse_data(self):
        pass

class Overall(Parser):
    def __init__(self, data, args):
        self.data = data
        self.countries = args

    def check_data(self):
        pass
    
    def parse_data(self):
        pass