from bs4 import BeautifulSoup
import ssl, urllib.request, re
from .Unit_of_Study import Unit_of_Study

WEBSITE_URL = "https://www.timetable.usyd.edu.au/uostimetables/2020/"

def return_html(classes, semester):
    # Fetches the selection page
    timetable_page = urllib.request.urlopen(WEBSITE_URL, context=ssl._create_unverified_context())
    parsed_html = BeautifulSoup(timetable_page, features= "html.parser")
    
    invalid_class_codes = []
    # Removes invalid unit codes
    for c in reversed(classes):
        if not re.match(r"^\w{4}\d{4}", c):
            invalid_class_codes.append(c)
            classes.remove(c)
    
    links = []
    # Checks all <a> tags and keeps the links to the ones we need
    for link in parsed_html.findAll('a', href=True):
        unit_name = link.contents[0].upper().strip()
        unit_element = link.parent.next_sibling
        unit_session = "" if unit_element == None else unit_element.text
        if(unit_name in classes) and (semester in unit_session):
            links.append(link["href"])
            classes.remove(unit_name)
    codes_not_found = classes
    
    HTML = []
    for link in links:
        b = urllib.request.urlopen(WEBSITE_URL+link, context=ssl._create_unverified_context()).read()
        HTML.append(str(b))

    return invalid_class_codes, codes_not_found, HTML


def return_units(html_array):

    units = []
    for unit_html in html_array:
        parsed_html = BeautifulSoup(unit_html, features="html5lib")

        # Select highest level tables that contain the info we need
        all_tables = parsed_html.find_all("table", attrs={"cellpadding": "3"})

        # Remove the 'weeks' display sub-table
        for table in all_tables:
            to_remove = table.find_all("div")
            to_remove += table.find_all("td", attrs={"colspan": "4"})
            weeks_text = table.find_all("div", {"class": "weeks"})
            for t in to_remove:
                # Keep weeks text, but remove date breakdown and other unnecesary stuff
                if t in weeks_text:
                    for x in t.find_all("span"):
                        x.extract()
                else:
                    t.parent.extract()

        # Use the first table, which is all the info, to create the unit object
        current_unit = Unit_of_Study(all_tables[0])

        # Add classes to unit
        for table in all_tables[1:]:
            current_unit.add_class(table)
        
        units.append(current_unit)
    
    return units



    
