""" database dependencies to support Users db examples """
from random import randrange

from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the 'Users Notes' table  with a relationship to Users within the model
class Notes(db.Model):
    __tablename__ = 'notes'

    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, unique=False, nullable=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.userID'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, note, userID):
        self.note = note
        self.userID = userID

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    def __repr__(self):
        return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "note": self.note,
            "userID": self.userID
        }


class Matches(UserMixin, db.Model):
    __tablename__ = 'matches'

    # Define the Users schema
    gameID = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(255), unique=False, nullable=False)
    team1 = db.Column(db.String(255), unique=False, nullable=False)
    team2 = db.Column(db.String(255), unique=False, nullable=False)
    winner = db.Column(db.String(255), unique=False, nullable=False)
    score = db.Column(db.String(255), unique=False, nullable=False)
    url = db.Column(db.String(255), unique=False, nullable=False)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, date, team1, team2, winner, score, url):
        self.date = date
        self.team1 = team1
        self.team2 = team2
        self.winner = winner
        self.score = score
        self.url = url

    # returns a string representation of object, similar to java toString()
    def __repr__(self):
        return "Matches(" + str(self.gameID) + "," + self.date + "," + str(self.team1) + "," + str(
            self.team2) + "," + str(self.winner) + "," + str(self.score) + "," + str(self.url) + ")"

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            #db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "gameID": self.gameID,
            "date": self.date,
            "team1": self.team1,
            "team2": self.team2,
            "winner": self.winner,
            "score": self.score,
            "url": self.url,

        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, date):
        """only updates values with length"""
        if len(date) > 0:
            self.date = date

        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


# Define the Users table within the model
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) Users represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    # Define the Users schema
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    phone = db.Column(db.String(255), unique=False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    notes = db.relationship("Notes", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes of instance variables within object
    def __init__(self, name, email, password, phone):
        self.name = name
        self.email = email
        self.set_password(password)
        self.phone = phone

    # returns a string representation of object, similar to java toString()
    def __repr__(self):
        return "Users(" + str(self.userID) + "," + self.name + "," + str(self.email) + ")"

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from Users(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "query": "by_alc"  # This is for fun, a little watermark
        }

    # CRUD update: updates users name, password, phone
    # returns self
    def update(self, name, password="", phone=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(password) > 0:
            self.set_password(password)
        if len(phone) > 0:
            self.phone = phone
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None

    # set password method is used to create encrypted password
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    # check password to check versus encrypted password
    def is_password_match(self, password):
        """Check hashed password."""
        result = check_password_hash(self.password, password)
        return result

    # required for login_user, overrides id (login_user default) to implemented userID
    def get_id(self):
        return self.userID


"""Database Creation and Testing section"""


# Builds working data for testing
def model_builder():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = Users(name='Adi Khandelwal', email='ak@g', password='1', phone="1")
    u2 = Users(name='Rohan Gaikwad', email='rg@g', password='1', phone="1")
    u3 = Users(name='Samaya Sankuratri', email='ss@g', password='1', phone="1")
    u4 = Users(name='Arch Huang', email='ah@g', password='1', phone="1")
    u5 = Users(name='Daniel Levy', email='dl@g', password='1', phone="1")
    table = [u1, u2, u3, u4, u5]

    """Builds sample user/note(s) data"""
    for row in table:
        try:
            '''add a few 1 to 4 notes per user'''
            for num in range(randrange(1, 4)):
                note = "#### " + row.name + " note " + str(num) + ". \n Generated by test data."
                row.notes.append(Notes(note=note, userID=row.userID))
            '''add user/note data to table'''
            db.session.add(row)
            db.session.commit()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {row.email}")

    g1 = Matches(date='3/1/2022', team1='Del Norte', team2='Mission Hills', winner="Del Norte", score="16-2", url="https://app.universaltennis.com/events/92708")
    table2 = [g1]



    for row1 in table2:
        try:
            '''add user/note data to table'''
            db.session.add(row1)
            db.session.commit()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print("Faulty match")


# Looks into database
def model_driver():
    print("---------------------------")
    print("Create Tables and Seed Data")
    print("---------------------------")
    model_builder()

    print("---------------------------")
    print("Table: " + Users.__tablename__)
    print("Columns: ", Users.__table__.columns.keys())
    print("---------------------------")
    print("Table: " + Notes.__tablename__)
    print("Columns: ", Notes.__table__.columns.keys())
    print("---------------------------")
    print()

    users = Users.query
    for user in users:
        print("User" + "-" * 81)
        print(user.read())
        print("Notes" + "-" * 80)
        for note in user.notes:
            print(note.read())
        print("-" * 85)
        print()

        games = Matches.query
    for game in games:
        print("Game:" + "-" * 81)
        print(game.read())
        print("Games" + "-" * 80)



if __name__ == "__main__":
    model_driver()
