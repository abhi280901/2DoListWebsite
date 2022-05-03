from flask import Flask, render_template
app = Flask(__name__)

#route to the index
@app.route('/')
def index():
    return render_template('layout.html')

#route to the index
@app.route('/logo')
def logo():
    return render_template('logo.html')


#route to the index
@app.route('/reg')
def reg():
    return render_template('reg.html')

#route to the index
@app.route('/home')
def home():
    return render_template('hm.html')

#route to the index
@app.route('/groc')
def groc():
    return render_template('groc.html')

#route to the index
@app.route('/share')
def share():
    return render_template('share.html')

#route to the index
@app.route('/mail')
def mail():
    return render_template('mbox.html')

#route to the index
@app.route('/rec')
def rec():
    return render_template('rec.html')

#route to the index
@app.route('/com')
def com():
    return render_template('comp.html')
