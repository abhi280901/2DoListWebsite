from flask import Flask, request, redirect, render_template, session
app = Flask(__name__)
app.secret_key = 'any Su93r$3cret string you want'

@app.route('/')
def method():
    if 'username' in session:
        username = session['username']
        return f'Logged in as {username}<br>'+\
                '<b><a href="/logout">Logout</a>'
    
    return 'You need to log in<br>'+\
            '<b><a href="/login">Login</a>'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username']=request.form['username']
        return redirect('/')

    # render the login page
    return render_template('session1.html')

@app.route('/logout')
def logout():

    # for a single item
    # either
    # 1. delete the username from the session (Error if the key isn't there)
    #try:
     #   del session['username']
    #except KeyError:
     #   pass

    # 2. pop the username (None is returned if key isn't there)
    #session.pop('username',None)

    # otherwise you might want to clear the session data (all of it!)
    session.clear()

    # a go back to the home page
    return redirect('/')

