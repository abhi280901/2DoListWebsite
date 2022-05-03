# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from flask_login import LoginManager, login_user

# create the Flask app
from flask import Flask, render_template, redirect, session
app = Flask(__name__)
app.secret_key = 'any Su93r$3cret string you want'


#import the request library
from flask import request

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up a 'model' for the data you want to store
from db_schema import db, User, List, ListItem, dbinit

# init the database so it can connect with our app
db.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = False
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()


#route to the index
@app.route('/')
def index():
    items = ListItem.query.all()
    lists = List.query.all()
    return render_template('layout.html', lists=lists, items=items)

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form["uname"]
        password = request.form["pswrd"]
        user = User.query.filter_by(username=username).first()
        if user == None:
            return redirect('/')
        else:
            if user.verify_password(password):
                # password is good so it is possible to login
                session['userid'] = user.id
                return redirect('/home')
            else:
                return redirect('/')

        
@app.route('/logout',  methods = ['GET','POST'])
def logout():
    session.pop('userid', None)
    return redirect('/')

#route to the index
@app.route('/logo')
def logo():
    return render_template('logo.html')


#route to the index
@app.route('/reg',  methods = ['GET','POST'])
def reg():
    if request.method == 'POST':
        hashed_password = security.generate_password_hash(request.form["pswrd"])
        user = User(request.form["first-name"], request.form["last-name"], request.form["uname"], hashed_password, request.form["email"],1)
        db.session.add(user)
        db.session.commit()
        return redirect('/usr')
    else:
        return render_template('reg.html')
    

#route to the index
@app.route('/home')
def home():
    userid = session.get('userid')
    lists = List.query.filter_by(user_id=userid).all()
    user = User.query.filter_by(id=userid).first()
    return render_template('hm.html',lists=lists,user = user)

#route to the index
@app.route('/groc')
def groc():
    list_id = request.args.get("id")
    lists = List.query.get(list_id)
    uncom_items = ListItem.query.filter_by(list_id=list_id,done=0).all()
    com_items = ListItem.query.filter_by(list_id=list_id,done=1).all()
    return render_template('groc.html',lists=lists, uncom_items=uncom_items,com_items=com_items)


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
@app.route('/usr')
def com():
    user = User.query.all()
    return render_template('user.html', user=user)

@app.route('/add', methods = ['GET','POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        numitem = request.form['numitem']
        userid = session.get('userid')
        newlist = List(name,numitem,userid)
        db.session.add(newlist)
        db.session.commit()
        lists = List.query.all()
        return redirect('/home')
    else:
        return render_template('additem.html')


