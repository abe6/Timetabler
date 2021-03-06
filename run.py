#-----------------------------------------------------------------------------
# This template is a variation from the template given to us for 
# INFO222, assignment 1, semester 1 2019
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Import bottle and site components
#-----------------------------------------------------------------------------
from bottle import run
import os

import model
import view
import controller

#-----------------------------------------------------------------------------
# Server config
#-----------------------------------------------------------------------------
# Change this to IP address or 0.0.0.0 when actually hosting
host = 'localhost'

# Test port, change to the appropriate port to host
port = 8080

# Turn this off for production
debug = True

# Auto reload after changes
reloader = True

#-----------------------------------------------------------------------------
# Running the server
#-----------------------------------------------------------------------------

if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host=host, port=port, debug=debug, reloader=reloader)