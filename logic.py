import itertools, html, math

"""
    HELPER FUNCTIONS
"""
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

        # Tracks points for each day in the week [mon, tues, wed, thur, fri]
        daily_points = [0,0,0,0,0]
        # Tracks how many classes per day [mon, tues, wed, thur, fri]
        daily_classes = [0,0,0,0,0]

        # Here each class is scored based on its start time and class type
        for session in week:
            # Points for this session
            points = 0

            # Add the start time, later start times are more favourable
            points += session["start"] ** 2

            # Lectures are favourbale and score higher because they are skipable lol
            if session["type"].lower() in ['lecture', "lec", "l"]:
                points += 100

            # Add this sessions points to the day(s) it is on 
            # and also +1 classes for that day
            for day in session["days"]:
                day = day.lower()
                if day == "mon":
                    daily_classes[0] += 1
                    daily_points[0] += points
                elif day == "tue":
                    daily_classes[1] += 1
                    daily_points[1] += points
                elif day == "wed":
                    daily_classes[2] += 1
                    daily_points[2] += points
                elif day == "thu":
                    daily_classes[3] += 1
                    daily_points[3] += points
                elif day == "fri":
                    daily_classes[4] += 1
                    daily_points[4] += points
                else:
                    print("DAY ERROR: " + day)
                    exit(0)
        
        # Measure of how spread out the classes are over the days
        # Smaller variance is more favourable
        """
            idk if this is even right but its all i could come up with, 
            basically non-zero is daily_classes but with all the 0's removed, so it may look like [2,4,5]. 
            These numbers are then all multiplied by eachother. The idea is that weeks with the same number
            of classes can get different scores based on if the classes are bulked into one day or not. eg 
            [3, 3, 3, 3, 3] = 243, [5, 1, 4, 2, 3] = 120, therefore the second one is more favourable, 
            even though they both have the same number of classes.
        """
        non_zero = [float(v) for v in daily_classes if v != 0]
        variance = 1
        for x in non_zero:
            variance *= x

        # Final score, higher is better, therefore you want a high daily_point and low variance
        """
            maybe max(daily_points) should change to a sum or maybe a product?
            i feel like i had that before but it didn't work i don't remember why - needs more investigation
        """
        score = max(daily_points) - (variance ** 2)

        # Convert the week (currently a tuple) to a list so it can be mutated
        weekAsList = list(week)

        # Sort the week by start time so its in a good order
        weekAsList.sort(key = lambda x: x["start"])

        # Add the score to the end of the week
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
        "results": []
    }
    for week in best_scorers:
        week_final = {
            "Mon" : [],
            "Tue": [],
            "Wed": [],
            "Thu": [],
            "Fri": []
        }
        # Every class is formated then added to the relevant days
        for session in week:
            if type(session) == float:
                continue
                
            s = "{}: {}-{}".format(session["name"], display_time(session["start"]), display_time(session["end"]))
            # Safety first ;)
            s = html.escape(s)
            
            for day in session["days"]:
                week_final[day].append(s)
        # The week_final is added to the response
        response["results"].append(week_final)

    # All done yay
    return response