import itertools, html

def is_Collision(session, other):

    for day in session["days"]:
        if day in other["days"]:
            if(max(session["start"], other["start"]) < min(session["end"], other["end"])):
                return True
            else:
                return False
    return False

def convert_times(start, end):
    newStart = int(start.replace(":", ""))
    newEnd = newStart + 100 if end == None else int(end.replace(":", ""))
    return newStart, newEnd

def display_time(time):
    time = str(time)
    return time[:-2] + ":" + time[-2:]

def already_contains(item, entire):
    for x in entire:
        if x["days"] == item["days"] and x["start"] == item["start"]:
            return True
    return False

def do_work(classes):

    response = {
        "results": [],
        "error": None
    }
    all_options = []
    for _name, class_ in classes.items():
        current_options = []
        for o in class_["options"]:
            o["type"] = class_["type"]
            o["name"] = class_["name"]
            o["start"], o["end"] = convert_times(o["start"], o["end"])
            # Only consider if its not a dupe
            if not already_contains(o, current_options):
                current_options.append(o)
        all_options.append(current_options)

    print(all_options)
    results = list(itertools.product(*all_options))

    best_days = 8
    least_days = []
    for week in reversed(results):
        # Iterates over all possible results, 
        # and only keeps those with the least number of days, 
        # removing the rest
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

    no_collisions = []
    for week in reversed(least_days):
        # Iterates over all remaining options,
        # compares each session to every other session in that week,
        # removes the week if it contains a timing collision
        try:
            for i in range(len(week)):
                session = week[i]
                for j in range(i+1,len(week)):
                    other = week[j]
                    if not is_Collision(session, other):
                        no_collisions.append(week)
                        raise ValueError
        except ValueError:
            continue
    
    scored = []
    max_score = 0
    best_scorers = []
    for week in no_collisions:

        # Keep track of points for each day
        daily_points = [0,0,0,0,0]

        # Tracks how many classes per day
        daily_classes = [0,0,0,0,0]

        for session in week:
            # Points for this session
            points = 0

            # Add the start time, later start times are more favourable
            points += session["start"] * 2

            # Lectures are more favourable, more skipable
            if session["type"].lower() in ['lecture', "lec", "l"]:
                points += 10

            # Add sessions points to all days the session is on
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
        non_zero = [float(v) for v in daily_classes if v != 0]
        variance = 1
        for x in non_zero:
            variance *= x

        # Final score, higher is better
        score = max(daily_points) - variance

        weekAsList = list(week)

        # Sort by start time
        weekAsList.sort(key = lambda x: x["start"])

        # Add the score
        weekAsList.append(score)
        
        # Keep track of those that have the highest score
        if score > max_score:
            max_score = score
            best_scorers = [weekAsList]
        elif score == max_score:
            best_scorers.append(weekAsList)

        # Add all to the 'scored' list
        scored.append(weekAsList)
    
    #format response
    for week in best_scorers:
        days = {
            "Mon" : [],
            "Tue": [],
            "Wed": [],
            "Thu": [],
            "Fri": []
        }
        
        for session in week:
            if type(session) == float:
                continue
            s = "{}: {}-{}".format(session["name"], display_time(session["start"]), display_time(session["end"]))
            for day in session["days"]:
                days[day].append(s)
        response["results"].append(days)

    return response