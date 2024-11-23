
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


class Interactive(Parser):
    def __init__(self, data):
        self.data = data

    def check_data(self):
        pass
    
    def parse_data(self, country):
        class Olympiad():
            def __init__(self, city=''):
                self.city = city
                self.total_medals = 0
                self.medals = {
                    'Gold': 0,
                    'Silver': 0,
                    'Bronze': 0
                }
            def add_medal(self, medal):
                if medal != 'NA':
                    self.medals[medal] += 1
                    # print(self.medals)
                self.total_medals += 1
            def get_medals_count(self):
                return self.medals
            def get_total_medals(self):
                return self.total_medals
            def get_city(self):
                return self.city
            def __lt__(self, other_olympiad):
                return self.total_medals < other_olympiad.total_medals

        years = {}
        self.medals = []
        for row in self.data:
            if not row['Team'] == country and not row['NOC'] == country:
                continue
            if not int(row['Year']) in years:
                years[int(row['Year'])] = Olympiad(row['City'])
            years[int(row['Year'])].add_medal(row['Medal'])

        worst_olympiad = min(years, key=years.get)
        best_olympiad = max(years, key=years.get)
        first_olympiad = min(list(years.keys()))

        avg_medals = Olympiad().get_medals_count()
        for olympiad in years.values():
            medals = olympiad.get_medals_count()
            for medal, count in medals.items():
                avg_medals[medal] += count
        for medal, count in avg_medals.items():
            avg_medals[medal] //= len(years)
        
        self.table_header = "{:20s} | \t {:5s} |\t {:15s} |\t {}\n".format("Type", "Year", "City", "Medals")
        self.table = "{:20s} | \t {:5s} |\t {:15s} |\t {}\n".format(
            "First Olympiad", str(first_olympiad), years[first_olympiad].get_city(), years[first_olympiad].get_total_medals())
        self.table += "{:20s} | \t {:5s} |\t {:15s} |\t {}\n".format(
            "Best Olympiad", str(best_olympiad), years[best_olympiad].get_city(), years[best_olympiad].get_total_medals())
        self.table += "{:20s} | \t {:5s} |\t {:15s} |\t {}\n".format(
            "Worst Olympiad", str(worst_olympiad), years[worst_olympiad].get_city(), years[worst_olympiad].get_total_medals())
        self.table += "\n{}\n{:25s} {:10s} |\t {:10s} |\t {:10s}\n".format(
            "Avarage Number of Medals:", '', "Gold", "Silver", "Bronze") 
        self.table += "{:25s} {:10s} |\t {:10s} |\t {:10s}".format(
            '', str(avg_medals["Gold"]), str(avg_medals["Silver"]), str(avg_medals["Bronze"])) 
