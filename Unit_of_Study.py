from Unit_Class import Unit_Class
from bs4 import BeautifulSoup

class Unit_of_Study(object):
    def __init__(self, table):

        # Parse table
        text = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            text.append([ele for ele in cols if ele]) # Get rid of empty values

        self.code = text[1][1]
        self.name = text[2][1]
        self.semester = " ".join([text[3][1] , text[0][1]])
        self.delivery_mode = text[4][1]
        self.campus = text[5][1]
        self.classes = []
    
    def __repr__(self):
        string = """
    + Unit Name: {}
    + Unit Code: {}
    + Semester: {}
    + Delivery: {}
    + Campus: {}
    + Classes: {}\n""".format(self.name, self.code, self.semester, self.delivery_mode, 
        self.campus, self.classes)
        return string

    def add_class(self, table):
        info = table.find('td').text.split()
        new_class = Unit_Class(info[1], " ".join(info[2:]))

        options = table.find_all("table")
        cleaned = []
        for option in options:
            o = []
            for row in option.find_all('tr'):
                x = [y.get_text() for y in row.find_all('td')]
                o.append([x[0], x[1]])
            cleaned.append(o)

        for option in cleaned:
            times = option[0][1].split("-")
            days = [x[0] for x in option]
            days = list(dict.fromkeys(days)) # Removes duplicate days
            new_class.add_option(days, times[0], times[1])
        
        self.classes.append(new_class)
