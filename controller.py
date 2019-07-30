from bottle import route, get, post, request, redirect, static_file
import glob, os
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

    # Get files
    files = request.files.getall("fileUpload")
    text = ""
    for f in files:
        # Save the files
        name, ext = os.path.splitext(f.filename)
        if ext in ('.htm','.html'):
            save_path = "tmp/"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file_path = "{path}/{file}".format(path=save_path, file=f.filename)
            f.save(file_path)
        
    # read them in, then delete it
    for filename in glob.glob(os.path.join("tmp/", '*.htm')):
        with open(filename, "r") as f:
            text = text + f.read()
        os.remove(filename)
                
    # Call the appropriate method
    return model.options(text)


