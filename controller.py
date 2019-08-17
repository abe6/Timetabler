from bottle import route, get, post, request, redirect, static_file
import model

#-----------------------------------------------------------------------------
'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    return static_file(picture, root='img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    return static_file(css, root='css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    return static_file(js, root='js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    return model.home_page()

@post('/fileSubmission')
def post_form():
    # Handles the form processing
    data = request.json

    unitCodes = data["codes"].split(",")
    unitCodes = [x.upper().strip() for x in unitCodes]

    # Call the appropriate method
    return model.options(unitCodes, data["semester"])


