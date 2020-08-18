import re

class Unit_Class(object):

    def __init__(self, unit, name, typee):
        self.name = unit.code + " " + name
        self.typee = typee
        self.options = []
        self.unit = unit

        """
        VARIABLES
        """
        # Applied to a sessions score if its online
        self.ONLINE_BONUS = 10
        # Score per type of class
        self.TYPE_SCORES = {
            "lec":5,
            "lecture":5,
            "tute":3,
            "tutorial":3,
            "practical":1
        }

    
    def __repr__(self):
        string = """
        * Class Name: {}
        * Class Type: {}
        * Options: {}\n""".format(self.name, self.typee, self.options)
        return string
    
    # Converts times from strings in the format hh:mm to an int with format hhmm
    def convert_times(self, time):
        return int(time.replace(":", ""))

    # Converts [1,5] to [1,2,3,4,5]
    def range_from_pair(self, pair):
        if len(pair) != 2:
            return None
        return list(range(int(pair[0]), int(pair[-1])+1))

    # Converts '[wks 1 to 5]' to [1,2,3,4,5]
    # Needs to handle formats '[wks 1]', '[wks 1 to 3, 5 to 7, 8 to 10]' also
    def convert_weeks(self, weeks):
        nums = re.findall(r'\d+', weeks)
        if len(nums) > 2 and (len(nums) % 2 == 0): # Multiple pairs of number
            total = []
            for i in range (0, len(nums)-1, 2):
                total += self.range_from_pair([nums[i], nums[i+1]])
            return total
        elif len(nums) == 2: # Single pair 
            return self.range_from_pair(nums)
        if len(nums) == 1: 
            return nums
        else:
            return None
    
    def score_option(self, class_type, room):
        score = 0
        if "online" in room.lower():
            #print("Online bonus appled to '" + session["room"] + "'")
            score += self.ONLINE_BONUS

        # Test the last word in the class title to find a match with something that has a score
        type_test = class_type.lower().strip().split()[-1]
        add = self.TYPE_SCORES.get(type_test, None)
        if(add == None):
            print("TYPE NOT SEEN BEFORE == " + type_test)
            pass
        else:
            score += add

        return score

    def add_option(self, class_type, option_code, option_times):
        parsed_option = []
        for component in option_times:
            times = component[1].split("-")
            parsed_component = ({
                "type":class_type,
                "code":option_code,
                "score":self.score_option(class_type, component[3]),
                "day":component[0],
                "start":self.convert_times(times[0]),
                "end":self.convert_times(times[1]),
                "weeks":self.convert_weeks(component[2]),
                "room":component[3]
            })
            parsed_option.append(parsed_component)

        self.options.append(parsed_option)
    