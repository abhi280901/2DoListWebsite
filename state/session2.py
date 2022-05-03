from flask import Flask, request, redirect, render_template, session
from werkzeug import security

app = Flask(__name__)
app.secret_key = 'any Su93r$3cret string you want'

# normally store these in the database
password_database={
    'Kate':security.generate_password_hash("them"),
    'Andrew':security.generate_password_hash("heavy"),
    'Peter':security.generate_password_hash("people")
}
# 

@app.route('/')
@app.route('/badlogin')
def homepage():
    badlogin = ''
    if request.path=='/badlogin':
        badlogin="Login failed<br>"
    if 'username' in session:
        username = session['username']
        return f'Logged in as {username}<br>'+\
                '<b><a href="/logout">Logout</a>'
    
    return badlogin+'You need to log in<br>'+\
            '<b><a href="/login">Login</a>'


@app.route('/viewpasswords')
def view():
    allpw = ''
    for k,v in password_database.items():
        allpw += f"{k}: {v}<br><br>"

    return allpw
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
       
        hashed_password = password_database[username] if username in password_database else None

        if hashed_password and security.check_password_hash(hashed_password, password):
            # password is good so it is possible to login
            session['username']=request.form['username']
            return redirect('/')
        else:
            return redirect('/badlogin')

    # render the login page
    return render_template('session2.html')

@app.route('/logout')
def logout():

    # for a single item
    # either
    # 1. delete the username from the session (Error if the key isn't there)
    try:
        del session['username']
    except KeyError:
        pass

    # 2. pop the username (None is returned if key isn't there)
    session.pop('username',None)

    # otherwise you might want to clear the session data (all of it!)
    session.clear()

    # a go back to the home page
    return redirect('/')

