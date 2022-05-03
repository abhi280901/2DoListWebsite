# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# create the database interface
db = SQLAlchemy()

# a model of a forum for the database
class Forum(db.Model):
    __tablename__='forums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    headline = db.Column(db.Text())

    def __init__(self, name, headline):
        self.name=name
        self.headline=headline


# a model of a forum for the database
class Thread(db.Model):
    __tablename__='threads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    message = db.Column(db.Text())
    created_at = db.Column(db.DateTime())
    forum_id = db.Column(db.Integer(), db.ForeignKey('forums.id') )

    def __init__(self, title, message, created_at, forum_id):
        self.title=title
        self.message=message
        self.created_at=created_at
        self.forum_id=forum_id



from datetime import datetime
import time

def dbinit():
    db.session.add(Forum("Lab Sessions", "Discuss Lab Sessions here"))
    db.session.add(Forum("Lectures", "Discuss lectures here"))
    db.session.add(Forum("General", "Discuss anything else here"))

    posttime = datetime(2022,2,4,18,0)
    
    db.session.add(Thread("Lab 2 help", "Anybody good at CSS?",posttime,1))
    db.session.add(Thread("Can you smell doughnuts?", "I think so",posttime,1))
    db.session.add(Thread("Python win", "This is true",posttime,1))

    time.sleep(1)
    db.session.add(Thread("Great lecture", "Best. Lecture. Ever!", datetime.now(),2))
    time.sleep(1)
    db.session.add(Thread("I LOVE CS139", "It is so good", datetime.now(),2))

    db.session.commit()