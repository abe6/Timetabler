import itertools, html, math

"""
Variables for the scoring process
"""
COLLISION_PENALTY = -100

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

# Returns a dictionary containing the number of classes on each day
# Only contains the day for which the count is > 0
def count_days(week):
    days = {}
    for session in week:
        current = days.get(session["day"])
        days[session["day"]] = 1 + current if (current != None) else 1
    print(week)
    print(days)
    return days

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

        score = 0

        score += COLLISION_PENALTY if is_Collision(week) else 0
        score -= len(count_days(week)) ** 3

        # Store the weeks index and score
        scored[index] = score
    
    return {}