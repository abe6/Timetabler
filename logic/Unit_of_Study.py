from .Unit_Class import Unit_Class
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

    def getInfo(self): 
        return [self.name, self.code, self.semester, self.delivery_mode, self.campus]

    def add_class(self, table):
        
        info = table.find('td').text.split()
        new_class = Unit_Class(self, info[1], " ".join(info[2:]))

        class_type = table.find("strong").get_text(separator=' ')
        rows = table.find("tbody").find_all("tr", recursive=False)

        for i in range(2, len(rows)):
            row = rows[i]
            option_code = row.find('td').get_text(separator=' ')
            if "closed" in option_code.lower():
                continue # Don't process options that are closed
            option_times = []
            for timeslot in row.find_all("tr"):
                if len(timeslot.find_all("tr")) != 0: 
                    continue # Skip top level rows (ones with other rows inside)
                else: # Else add the option to the list
                    x = [x.get_text().strip() for x in timeslot.find_all("td")]
                    option_times.append(x)
            new_class.add_option(class_type, option_code, option_times)
        
        self.classes.append(new_class)
