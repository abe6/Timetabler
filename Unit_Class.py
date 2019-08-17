class Unit_Class(object):

    def __init__(self, name, typee):
        self.name = name
        self.typee = typee
        self.options = []
    
    def __repr__(self):
        string = """
        * Class Name: {}
        * Class Type: {}
        * Options: {}\n""".format(self.name, self.typee, self.options)
        return string
    
    # Converts times from strings in the format hh:mm to an int with format hhmm
    def convert_times(self, time):
        return int(time.replace(":", ""))
    
    def add_option(self, days, start, end):
        op = {"days": days, "start": self.convert_times(start), 
            "end": self.convert_times(end), "name": self.name, "type": self.typee}
        for o in self.options:
            if (o["days"] == op["days"]) and (o["start"] == op["start"]) and (o["end"] == op["end"]):
                return
        self.options.append(op)
    