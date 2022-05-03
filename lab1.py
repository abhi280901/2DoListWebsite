from flask import Flask, render_template
app = Flask(__name__)

#route to the index
@app.route('/')
def index():
    return render_template('index.html')


#route to the index
@app.route('/reg')
def reg():
    return render_template('registration.html')

#route to the index
@app.route('/home')
def home():
    return render_template('home.html')

#route to the index
@app.route('/groc')
def groc():
    return render_template('groceries.html')

#route to the index
@app.route('/share')
def share():
    return render_template('shared.html')

#route to the index
@app.route('/mail')
def mail():
    return render_template('mail.html')

#route to the index
@app.route('/rec')
def rec():
    return render_template('record.html')

#route to the index
@app.route('/com')
def com():
    return render_template('compose.html')
