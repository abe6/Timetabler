'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import logic, parser

# Initialise our views, all arguments are defaults
page_view = view.View()

#-----------------------------------------------------------------------------
# Home
#-----------------------------------------------------------------------------

def home_page():
    return page_view("home")

def options(unitCodes, semester):
    # codes should be an array of strings, and semester a single digit string e.g "2"
    invalid_class_codes, codes_not_found, HTML = parser.return_html(unitCodes, semester)
    
    units = parser.return_units(HTML)
    response = logic.do_work(units)

    response["invalid"] = invalid_class_codes
    response["notFound"] = codes_not_found
    
    return response