import itertools, html, math

"""
Variables for the scoring process
"""
# Applied once per week, if there exists a collision
COLLISION_PENALTY = -100
# Applied once per week. Num days needed to attend, to the power of
DAY_MULTI = 4 
# Applied once per week. Average start time, to the power of
START_TIME_MULTI = 4

"""
    HELPER FUNCTIONS
"""
# Returns true if there exist any collision in the week
def is_Collision(week):
    for x in range(0, len(week)+1):
        for y in range(x, len(week)+1):
            a = week[x]
            b = week[y]
            if (
                (a["day"] == b["day"]) and
                (a["start"] == b["start"]) and
                (a["end"] == b["end"])
                ):
                for w1 in a["weeks"]:
                    if w1 in b["weeks"]:
                        return True    
    return False

# Returns a dictionary containing another dictionary for each day there is at least 1 class
# e.g {"mon":{"count":x, "score":y)}
# Where x is the number of classes on that day, and
# y is the score based on the type of classes on that day
def count_days(week):
    days = {}
    for session in week:
        current = days.get(session["day"]) # The existing result for that day
        new_count = current["count"] + 1 if (current != None) else 1
        new_score = current["score"] + session["score"] if (current != None) else session["score"]

        # Update
        days[session["day"]] = {"count": new_count, "score": new_score}
    return days

# Returns the average start time (int) of the week 
def avg_start_time(week):
    days = {}
    for session in week:
        current = days.get(session["day"])
        new = session["start"]
        if current == None or current > new :
            days[session["day"]] = new
    avg = sum(days.values(), 0)/len(days)
    return math.floor(avg)

# Converts int time to string in format hh:mm
def display_time(time):
    time = str(time)
    return time[:-2] + ":" + time[-2:]

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
    
    # Scoring each permutation (week)
    scored = {}
    for index in range(0, len(results)):
        week = sum(results[index], []) # Flatten the list

        # High score is better
        score = 0

        # A dictionary containing the amount of classes for each day, and its type score
        daily_counts = count_days(week)
        print(week)
        print(daily_counts)
        print("--")

        score += COLLISION_PENALTY if is_Collision(week) else 0
        score -= len(daily_counts) ** DAY_MULTI # Lower is better, minimise days attended
        score += avg_start_time(week) ** START_TIME_MULTI # Higher is better, start later
        # Add type scores for each day, higher is better
        for day in daily_counts.values():
            score += day["score"]

        # TODO: score based on load spread

        # Store the weeks index and score
        scored[index] = score
    
    return {}