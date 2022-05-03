# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug import security
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user, login_required
from sqlalchemy import text
from markupsafe import escape

# create the Flask app
from flask import Flask, render_template, redirect, session, jsonify
app = Flask(__name__)
app.secret_key = 'any Su93r$3cret string you want'


#import the request library
from flask import request

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///todo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up a 'model' for the data you want to store
from db_schema import db, User, List, ListItem, dbinit

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
    
#route to the index
@app.route('/')
def index():
    items = ListItem.query.all()
    lists = List.query.all()
    return render_template('layout.html', lists=lists, items=items)

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = escape(request.form["uname"])
        password = escape(request.form["pswrd"])
        user = User.query.filter_by(username=username).first()
        if user == None:
            return redirect('/')
        else:
            if user.verify_password(password):
                # password is good so it is possible to login
                login_user(user)
                return redirect('/home')
            else:
                return redirect('/')

        
@app.route('/logout',  methods = ['GET','POST'])
def logout():
    logout_user()
    return redirect('/')

#route to the index
@app.route('/logo')
def logo():
    return render_template('logo.html')


#route to the index
@app.route('/reg',  methods = ['GET','POST'])
def reg():
    if request.method == 'POST':
        hashed_password = security.generate_password_hash(escape(request.form["pswrd"]))
        username = escape(request.form["uname"])
        user = User(escape(request.form["first-name"]), escape(request.form["last-name"]), username, hashed_password, escape(request.form["email"]),1)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=username).first()
        login_user(user)
        return redirect('/home')
    else:
        return render_template('reg.html')
    

#route to the index
@app.route('/home')
@login_required
def home():
    if current_user.is_authenticated:
        userid = current_user.id
        lists = List.query.filter_by(user_id=userid).all()
        user = User.query.filter_by(id=userid).first()
    return render_template('hm.html',lists=lists,user = user)

#route to the index
@login_required
@app.route('/groc')
def groc():
    list_id = escape(request.args.get("id"))
    userid = current_user.id
    lists = List.query.get(list_id)
    if lists.user_id == userid:
        uncom_items = ListItem.query.filter_by(list_id=list_id,done=0).all()
        com_items = ListItem.query.filter_by(list_id=list_id,done=1).all()
        return render_template('groc.html',lists=lists, uncom_items=uncom_items,com_items=com_items,list_id=list_id)
    else:
        return redirect('/logout')


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

@app.route('/additem', methods = ['GET','POST'])
@login_required
def additem():
    if request.method == 'POST':
        listitem = ListItem(escape(request.form['item']), escape(request.form['list']),0)
        db.session.add(listitem)
        db.session.commit()
        return "ble"
    #if request.method == 'POST':
     #   listitem = escape(request.form['item'])
      #  list_id = escape(request.form['list'])
       # qrytext = text("INSERT INTO items(name, list_id, done) VALUES (:listitem, :list_id, 0);")
        #qry = qrytext.bindparams(listitem=listitem, list_id=list_id)
        #db.session.execute(qry)
        #db.session.commit()
        #return redirect('/home')

@app.route('/updatetodone', methods = ['GET','POST'])
def upd1():
    if request.method == 'POST':
        item = request.form['todo_id']
        listitem = ListItem.query.filter_by(id=item).first()
        listitem.done = 1
        db.session.commit()
        return "ble"

@app.route('/updatetonone', methods = ['GET','POST'])
def upd():
    if request.method == 'POST':
        item = request.form['todo_id']
        listitem = ListItem.query.filter_by(id=item).first()
        listitem.done = 0
        db.session.commit()
        return "ble"



@app.route('/add', methods = ['GET','POST'])
@login_required
def add():
    if request.method == 'POST':
        name = escape(request.form['name'])
        numitem = escape(request.form['numitem'])
        userid = current_user.id
        newlist = List(name,numitem,userid)
        db.session.add(newlist)
        db.session.commit()
        lists = List.query.all()
        return redirect('/home')
    else:
        return render_template('additem.html')


