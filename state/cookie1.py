from flask import Flask, request, redirect
from flask import render_template, render_template_string, make_response
app = Flask(__name__)

cookie_lifespan = 30

# set the cookie from a query string
@app.route('/setcookie')
def setcookie():
    username=request.args.get('name')
    message=request.args.get('mesg')
   
    # using render_template_string rather than loading an HTML file - this creates a string
    # need to make_response because cookies are in the header of the response (and not in a string)
    resp = make_response(render_template_string("{{message}}<br><a href=\"/\">home</a>", \
            message=f'Responding to "{message}" sent by "{username}"'))

    resp.set_cookie('somecookie', username, max_age=cookie_lifespan) # max_age in seconds

    return resp


# set the cookie from a form
@app.route('/setcookie_post', methods=["POST"])
def setcookie_post():
    username=request.form['name']
    message=request.form['mesg']

    # using render_template_string rather than loading an HTML file - this creates a string
    # need to make_response because cookies are in the header of the response (and not in a string)
    resp = make_response(render_template_string("{{message}}<br><a href=\"/\">home</a>", \
            message=f'Responding to "{message}" sent by "{username}"'))

    resp.set_cookie('somecookie', username, max_age=cookie_lifespan) # max_age in seconds, default is the browser session

    return resp

# redirect the query string to a route
@app.route('/redirectcookie')
def redirectcookie():
    username=request.args.get('name')
    message=request.args.get('mesg')
    # using the URL routing method
    return redirect(f'/response/{message}/{username}')

# URL routing rather than a query string
@app.route('/response/<message>/<username>')
def response(message,username):

    # need to make_response because cookies are in the header of the response (and not in a string
    # as returned by render_template)
    resp = make_response(render_template('cookie1response.html',\
            message=f'Responding to "{message}" sent by "{username}"'))
    resp.set_cookie('usercookie', username, max_age=cookie_lifespan)
    return resp

# a simple form
@app.route('/cookie1')
def render_static():
    return render_template(f'cookie1.html')


@app.route('/')
def root():
    name = request.cookies.get('somecookie') or 'not found'
    user = request.cookies.get('usercookie') or 'not found'
    return render_template("cookie1.html",cookie_lifespan=cookie_lifespan,user=user, name=name)
