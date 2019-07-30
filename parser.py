from bs4 import BeautifulSoup

def return_json(text):

    parsed_html = BeautifulSoup(text, features="html.parser")
    
    # Select all rows underneath the table with class 'TblPartsAndclasses'
    table_rows = parsed_html.select("table#TblPartsAndclasses > tr")
    
    classes = {

    }
    currentClass = ""
    lastOption = None
    for row in table_rows:
        name = row.get('id')
        
        # Handle canceled classes
        if row.get('class') != None:
            innerText = row.get_text().strip()
            if "[Cancelled]" in innerText:
                classes[currentClass]["options"].remove(lastOption)

        # Found a row with a new class name
        if name != None:
            currentClass = name

            # Add the class to classes if its not already in there
            if name not in classes:
                classes[name] = {
                    "name" : name,
                    "type" : name.split(".")[-1],
                    "options": []
                }
            
            # Continue checking other rows
            continue
        
        # Check if this row contains an option, if it does, add it to the current class
        options = row.select("table[class='class-time-display'] td")
        if options != None:
            # Pull out option info
            days = []
            start = ""
            end = ""
            for option in options:
                o = option.string
                if o != None:
                    o = o.strip()
                    day, time = o.split()
                    days.append(day)
                    if "-" in time:
                        start, end = time.split("-")
                    else:
                        start = time
                        end = None
            # Create a new option and add it to the current class
            if len(days) > 0:
                newOption = {
                    "days" : days,
                    "start" : start,
                    "end" : end
                }
                classes[currentClass]["options"].append(newOption)
                lastOption = newOption
        
    return classes

