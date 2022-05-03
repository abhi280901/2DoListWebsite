####
# template from lab3
# 
 
# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# create the Flask app
from flask import Flask, render_template
app = Flask(__name__)

# select the database filename
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///cs139forum.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# set up a 'model' for the data you want to store
# import the database connection and the initialisation function
from forum_schema import db, dbinit
# import my tables
from forum_schema import Forum, Thread

# init the database so it can connect with our app
db.init_app(app)

# change this to False to avoid resetting the database every time this app is restarted
resetdb = True
if resetdb:
    with app.app_context():
        # drop everything, create all the tables, then put some data into the tables
        db.drop_all()
        db.create_all()
        dbinit()


#import the request library
from flask import request

# route to root
# display all the forums on this site
@app.route('/')
def forum_list():
    forums = Forum.query.all()
    s = ""
    for entry in forums:
        s += f"{entry.name}<br>"
    return s







# route to threads
# use a forum id to get a list of threads that have that forum id
@app.route('/threads')
def thread_list():
    forum_id = request.args.get("id")
    threads = Thread.query.filter_by(forum_id=forum_id).all()
    s = ""
   
    for entry in threads:
        s += f"{entry.title}<br>"
    return s



#
####

# route to the index
# show the list of forums on the site
@app.route('/site')
def site():
    forums = Forum.query.all()
    return render_template('site.html', forums=forums)

# route to forum
# show a list of threads on the forum
@app.route('/forum')
def forum():
    forum_id = request.args.get("id")
    forum = Forum.query.get(forum_id)
    threads = Thread.query.filter_by(forum_id=forum_id).all()
    return render_template('forum.html', forum=forum, threads=threads)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/threadsjoin')
def thread_join():
    forum_id = request.args.get("id")
    threads = Thread.query.join(Forum, Thread.forum_id==Forum.id).filter_by(id=forum_id).all()

    s = str( Thread.query.join(Forum, Thread.forum_id==Forum.id).filter_by(id=forum_id) )
    s += "<br><br>"

    for entry in threads:
        s += f"{entry.title}<br>"
    return s