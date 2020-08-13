import itertools, html, math

"""
    HELPER FUNCTIONS
"""
def avg(array):
    non_zero = [x for x in array if x !=0]
    return sum(non_zero) / len(non_zero) 


# If classA and classB are on the same days, checks to make sure their times do not overlap.
# Returns true if there is a collision.
def is_Collision(classA, classB):
    for day in classA["days"]:
        if day in classB["days"]:
            if(max(classA["start"], classB["start"]) < min(classA["end"], classB["end"])):
                return True
    return False

# Converts int time to string in format hh:mm
def display_time(time):
    time = str(time)
    return time[:-2] + ":" + time[-2:]

# Return true if 'item' is in wholeset
# Used for when 'item' is a class option, and wholeset is an array of options
def already_contains(item, wholeset):
    for x in wholeset:
        if x["days"] == item["days"] and x["start"] == item["start"]:
            return True
    return False


"""
    MAIN FUNCTION CALLED BY THE FLASK APP
"""
def do_work(units):

    all_options = []
    for unit in units:
        for c in unit.classes: 
            all_options.append(c.options)

    # Generate all combinations of options
    results = list(itertools.product(*all_options))

    # Iterates over all possible results, and only keeps those with the least number of days
    best_days = 8
    least_days = []
    for week in results:
        # Array hold all days that have a class on them
        days = []
        for session in week:
            for day in session["days"]:
                if day not in days:
                    days.append(day)
        if len(days) < best_days:
            best_days = len(days)
            least_days = [week]
        elif len(days) == best_days:
            least_days.append(week)

    # Iterates over all the weeks with the least days,
    # compares each session to every other session in that week,
    # only keeps the week if it does not contain a collision
    no_collisions = []
    for week in least_days:
        safe = True
        for i in range(len(week)):
            session = week[i]
            for j in range(i+1,len(week)):
                other = week[j]
                if is_Collision(session, other):
                    safe = False
        if safe:
            no_collisions.append(week)
    
    # SCORING ALGORITHM
    # All the remaining weeks that do not have collisions are scored.
    scored = []
    max_score = 0
    best_scorers = []
    for week in no_collisions:

        # Used for converting day into its array index
        indexes = {"mon":0, "tue":1, "wed":2, "thu":3, "fri":4}
        # Tracks points for each day in the week [mon, tues, wed, thur, fri]
        daily_points = [0,0,0,0,0]
        # Tracks how many classes per day [mon, tues, wed, thur, fri]
        daily_classes = [0,0,0,0,0]
        # Tracks the lowest start time for each day
        start_times = [2400,2400,2400,2400,2400]

        # Here each class is scored based on its start time and class type
        for session in week:

            # Lectures are favourbale and score higher because they are skipable lol
            lessonType = session["type"].lower()
            lecturePoints = 0
            for symbol in ['lecture', "lec"]:
                if (symbol in lessonType) or (lessonType in ["l"]):
                    lecturePoints = 10
                    break
            if lecturePoints == 0:
                lecturePoints = -10

            # For each day this class is on,
            # that day gets the lecture points &
            # that day gets +1 class count &
            # start time gets assessed to find the earliest for each day.
            for day in session["days"]:
                index = indexes[day.lower()]
                daily_points[index] += lecturePoints
                daily_classes[index] += 1
                if session["start"] < start_times[index]:
                    start_times[index] = session["start"]
        
        
        """
            explain load calculation (microstates) N!/n1!n2!...
            smaller load spread is better
        """
        numerator = math.factorial(sum(daily_classes))
        denominator = (math.factorial(daily_classes[0]) 
                        * math.factorial(daily_classes[1]) 
                        * math.factorial(daily_classes[2]) 
                        * math.factorial(daily_classes[3]) 
                        * math.factorial(daily_classes[4]))
        loadSpread = math.log( numerator / denominator ) + 1


        """
            Final score, higher is better, therefore you want low loadSpread and
            the highest day score and a high average start time.
            Day score weighs more than start_time.
        """
        score =( max(daily_points)**2 + avg(start_times) )/ loadSpread 

        # Convert the week (currently a tuple) to a list so it can be mutated
        weekAsList = list(week)

        # Sort the week by start time so its in a good order
        weekAsList.sort(key = lambda x: x["start"])

        # Add the score to the end of the week
        ## weekAsList.append(start_times)
        ## weekAsList.append(daily_points)
        weekAsList.append(score)
        
        # Keep track of those that have the highest score
        if score > max_score:
            max_score = score
            best_scorers = [weekAsList]
        elif score == max_score:
            best_scorers.append(weekAsList)

        # Add get added to the scored list
        scored.append(weekAsList)
    
    # Begin to formulate the response that gets passed back to the site via AJAX.
    response = {
        "results": [],
        "units": []
    }
    # Add weeks
    for week in best_scorers:
        ## print(week[-1], week[-2], avg(week[-2]), avg(week[-3]))
        week_final = {
            "Mon" : [],
            "Tue": [],
            "Wed": [],
            "Thu": [],
            "Fri": []
        }
        # Every class is formated then added to the relevant days
        for session in week:
            if type(session) not in [dict]:
                continue
                
            s = "{}: {}-{}".format(session["name"], display_time(session["start"]), display_time(session["end"]))
            # Safety first ;)
            s = html.escape(s)
            
            for day in session["days"]:
                week_final[day].append(s)
        # The week_final is added to the response
        response["results"].append(week_final)
    # Add unit information
    for unit in units:
        response["units"].append(unit.getInfo())

    # All done yay
    return response