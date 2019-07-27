import itertools, html

def is_Collision(session, other):
    for day in session[0]:
        if day in other[0]:
            if(max(session[1], other[1]) < min(session[2], other[2])):
                return True
            else:
                return False
    return False

def formatTime(time):
    t = '{:0>4}'.format(time)
    return t[:2] + ':' + t[2:]

def checkTime(time):
    t = '{:0>4}'.format(time)
    hour = int(t[:2])
    mins = int(t[2:])
    return ((hour > 24 or hour < 0) or (mins >= 60 or mins < 0)) 


def do_work(classes):
    classTypes = ["lecture", "tutorial", "lab", "prac", "other"]
    response = {
        "results": [],
        "error": None
    }
    all_options = []

    for c in classes:
        classOptions = []
        if c["name"].strip() == "":
            response["error"] = "Class names cannot be empty."
            return response
        elif c["type"] not in classTypes:
            response["error"] = "You must choose a valid class type for all classes."
            return response
        else:
            for option in c["options"]:
                try:
                    start = int(option["start"].replace(":", ""))
                    end = int(option["end"].replace(":", ""))
                except ValueError:
                    response["error"] = "Times must be in the format hh:mm and contain only numbers."
                    return response
                except:
                    response["error"] = "There is an error with your time input."
                    return response
                if checkTime(start) or checkTime(end):
                    response["error"] = "Invalid time input."
                    return response
                if start >= end:
                    response["error"] = "All start times must be before end times."
                    return response

                for day in option["days"]:
                    if day not in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
                        response["error"] = "All options must only have valid days."
                        return response 
                #reformat option and add to list
                classOptions.append([option["days"], start, end, html.escape(c["name"]), c["type"]])
        all_options.append(classOptions)

    results = list(itertools.product(*all_options))

    best_days = 8
    least_days = []
    for week in reversed(results):
        # Iterates over all possible results, 
        # and only keeps those with the least number of days, 
        # removing the rest
        days = []
        for session in week:
            for day in session[0]:
                if day not in days:
                    days.append(day)
        if len(days) < best_days:
            best_days = len(days)
            least_days = [week]
        elif len(days) == best_days:
            least_days.append(week)
        elif len(days) > best_days:
            results.remove(week)
            continue

    for week in reversed(least_days):
        # Iterates over all remaining options,
        # compares each session to every other session in that week,
        # removes the week if it contains a timing collision
        try:
            for i in range(len(week)):
                session = week[i]
                for j in range(i+1,len(week)):
                    other = week[j]
                    if is_Collision(session, other):
                        least_days.remove(week)
                        raise ValueError
        except ValueError:
            continue
    
    scored = []
    max_score = 0
    best_scorers = []
    for week in least_days:

        # Keep track of points for each day
        daily_points = [0,0,0,0,0]

        # Tracks how many classes per day
        daily_classes = [0,0,0,0,0]

        for session in week:
            # Points for this session
            points = 0

            # Add the start time, later start times are more favourable
            points += session[1]

            # Lectures are more favourable, more skipable
            if session[4] == 'lecture':
                points += 10

            # Add sessions points to all days the session is on
            for day in session[0]:
                if day == "monday":
                    daily_classes[0] += 1
                    daily_points[0] += points
                elif day == "tuesday":
                    daily_classes[1] += 1
                    daily_points[1] += points
                elif day == "wednesday":
                    daily_classes[2] += 1
                    daily_points[2] += points
                elif day == "thursday":
                    daily_classes[3] += 1
                    daily_points[3] += points
                elif day == "friday":
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
        weekAsList.sort(key = lambda x: x[1])

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
            "monday" : [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": []
        }
        
        for session in week:
            if type(session) == float:
                continue
            
            s = "{}: {}-{}".format(session[3], formatTime(session[1]), formatTime(session[2]))
            for day in session[0]:
                days[day].append(s)
        response["results"].append(days)

    return response