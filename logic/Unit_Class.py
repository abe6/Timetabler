import re

class Unit_Class(object):

    def __init__(self, unit, name, typee):
        self.name = unit.code + " " + name
        self.typee = typee
        self.options = []
        self.unit = unit
    
    def __repr__(self):
        string = """
        * Class Name: {}
        * Class Type: {}
        * Options: {}\n""".format(self.name, self.typee, self.options)
        return string
    
    # Converts times from strings in the format hh:mm to an int with format hhmm
    def convert_times(self, time):
        return int(time.replace(":", ""))

    # Converts '[wks 1 to 5]' to [1,2,3,4,5]
    def convert_weeks(self, weeks):
        nums = re.findall(r'\d+', weeks)
        return list(range(int(nums[0]), int(nums[-1])+1))
    
    def add_option(self, option):
        parsed_option = []

        for component in option:
            times = component[1].split("-")
            parsed_component = ({
                "day":component[0],
                "start":self.convert_times(times[0]),
                "end":self.convert_times(times[1]),
                "weeks":self.convert_weeks(component[2]),
                "room":component[3]
            })
            parsed_option.append(parsed_component)

        self.options.append(parsed_option)
    