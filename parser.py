from collections import defaultdict
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
            self.total_medals += 1

    def get_medals_count(self):
        return self.medals
    
    def get_total_medals(self):
        return self.total_medals
    
    def get_city(self):
        return self.city
    
    def __lt__(self, other_olympiad):
        return self.total_medals < other_olympiad.total_medals
    
class Parser:
    def __init__(self, data, outputfile=None):
        self.data = data
        self.outputfile = outputfile

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

        if len(self.medals) == 0:
            print("Not valid country or there was no olympiad in given year")
            return False

        if len(self.medals) < 10:
            print("Country has less then 10 medals")
            return

        self.table_header = "{:30s} | \t {:25s} |\t {}\n".format("Name", "Sport", "Medal")
        self.table = ""
        for medal in self.medals[:10]:
            self.table += f"{medal['Name']:30s} |\t {medal['Sport']:25s} |\t {medal['Medal']}\n"

        return True
    
class Total(Parser):
    def __init__(self, data, args):
        self.data = data
        self.year = args
    
    def parse_data(self):
        countries = {}
        self.medals = []
        for row in self.data:
            if not row['Year'] == self.year:
                continue
            if not row['Team'] in countries:
                countries[row['Team']] = Olympiad()
            countries[row['Team']].add_medal(row['Medal'])

        if len(countries) == 0:
            print(f"In the {self.year} year olympiad didn't take place")
            return False
        
        self.table_header = "{:25s} | \t {:10s} |\t {:10s} |\t {}\n".format("Country", "Gold", "Silver", "Bronze")
        self.table = ""
        for country, olympiad in sorted(countries.items(), reverse=True, key=lambda o: o[1]):
            if olympiad.get_total_medals() < 1:
                continue
            medals = olympiad.get_medals_count()
            self.table += "{:25s} | \t {:10s} |\t {:10s} |\t {}\n".format(
                country, str(medals['Gold']), str(medals['Silver']), str(medals['Bronze']))

        return True


class Overall(Parser):
    def __init__(self, data, args):
        self.data = data
        self.countries = args

    def parse_data(self):
        countries = defaultdict(dict)
        for row in self.data:
            if not row['Team'] in self.countries:
                continue
            if not row['Team'] in countries:
                countries[row['Team']][int(row['Year'])] = Olympiad()
            if not int(row['Year']) in countries[row['Team']]:
                countries[row['Team']][int(row['Year'])] = Olympiad()
            countries[row['Team']][int(row['Year'])].add_medal(row['Medal'])

        if len(countries) == 0:
            print("Some of the entered countries doesn't exist")
            return False
        
        countries_best_year = {}
        for country, years in countries.items():
            countries_best_year[country] = max(years, key=years.get)

        self.table_header = "{:25s} | \t {:5s} |\t {}\n".format("Country", "Year", "Total Medals")
        self.table = ""
        for country, year in countries_best_year.items():
            self.table += "{:25s} | \t {:5s} |\t {}\n".format(
                country, str(year), str(countries[country][year].get_total_medals()))
        return True

        



class Interactive(Parser):
    def __init__(self, data):
        self.data = data

    def parse_data(self, country):
        years = {}
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
        
        return True
