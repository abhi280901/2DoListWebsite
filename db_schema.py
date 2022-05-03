from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager, UserMixin, current_user,
    login_required, login_user, logout_user
)

# create the database interface
db = SQLAlchemy()
class SharedList(db.Model):
    __tablename__='sharedlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    def __init__(self, name):
        self.name=name


# a model of a user for the database
class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text())
    last_name = db.Column(db.Text())
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(1024))
    email = db.Column(db.Text())
    sharedlist_id = db.Column(db.Integer(), db.ForeignKey('sharedlists.id') )

    def __init__(self,first_name,last_name, username, password_hash, email, sharedlist_id):  
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.password_hash=password_hash
        self.email = email
        self.sharedlist_id=sharedlist_id

    def get(x):
        return x

    @property
    def password(self):
        raise AttributeError("Can't view password!")

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

# a model of a list for the database
# it refers to a user
class List(db.Model):
    __tablename__='lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    numitem = db.Column(db.Integer())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id') )  # this ought to be a "foreign key"

    def __init__(self, name, numitem, user_id):
        self.name=name
        self.numitem=numitem
        self.user_id = user_id

# a model of a list item for the database
# it refers to a list
class ListItem(db.Model):
    __tablename__='items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    list_id = db.Column(db.Integer(), db.ForeignKey('lists.id') )  # this ought to be a "foreign key"
    done = db.Column(db.Integer()) #0 if pending, 1 if done

    def __init__(self, name, list_id, done):
        self.name=name
        self.list_id=list_id
        self.done = done 


class SharedListItem(db.Model):
    __tablename__='shareditems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    sharedlist_id = db.Column((db.Integer), db.ForeignKey('sharedlists.id') )   # this ought to be a "foreign key"
    done = db.Column(db.Integer()) #0 if pending, 1 if done


    def __init__(self, name, sharedlist_id, done):
        self.name=name
        self.sharedlist_id=sharedlist_id
        self.done = done

# put some data into the tables
def dbinit():
    shared_list = [
        SharedList("Movie with friends")
    ]
    db.session.add_all(shared_list)
    
    
    movie_id = SharedList.query.filter_by(name="Movie with friends").first().id
    user_list = [
        User("Felicia","John","Felicia","strongpswrd","felicia@yahoo.com",movie_id), 
        User("Petra","Secha","Petra","strongpswrd","petra@yahoo.com",movie_id)
        ]
    db.session.add_all(user_list)

    shareditems_list = [
        SharedListItem("Uncharted",movie_id,0),
        SharedListItem("No Way Home",movie_id,0),
        SharedListItem("Moonfall",movie_id,1),
    ]

    db.session.add_all(shareditems_list)

    # find the id of the user Felicia
    felicia_id = User.query.filter_by(username="Felicia").first().id

    all_lists = [
        List("Shopping",3,felicia_id), 
        List("Chores",3,felicia_id)
        ]
    db.session.add_all(all_lists)

    # find the ids of the lists Chores and Shopping

    chores_id = List.query.filter_by(name="Chores").first().id
    shopping_id= List.query.filter_by(name="Shopping").first().id

    all_items = [
        ListItem("Potatoes",shopping_id,0), 
        ListItem("Shampoo", shopping_id,0),
        ListItem("Apples", shopping_id,1),
        ListItem("Wash up",chores_id,0), 
        ListItem("Vacuum bedroom",chores_id,1),
        ListItem("Sweeping",chores_id,1)
        ]
    db.session.add_all(all_items)

    # commit all the changes to the database file
    db.session.commit()
